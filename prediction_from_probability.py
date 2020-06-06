import requests as rq
import pandas as pd
import numpy as np
import pickle
import os


def download_data(date, end, apikeys=None, peroid='1HRS'):
    if not apikeys:
        apikeys = load_api_keys()
    url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/history?period_id={}&' + \
          'time_start={}&time_end{}&limit=7317'
    if type(apikeys) == list:
        headers = {'X-CoinAPI-Key': apikeys[0]}
    else:
        headers = {'X-CoinAPI-Key': apikeys}
    response = rq.get(url.format(peroid, date, end), headers=headers)
    if response.status_code != 200:
        apikeys = select_apikey(apikeys)
        return download_data(date, end, apikeys)
    df = pd.DataFrame(response.json())
    df = df.filter(['time_open', 'time_close', 'price_close', 'price_open'])
    df['time_open'] = pd.to_datetime(df['time_open'].str.slice(stop=16))
    df['time_close'] = pd.to_datetime(df['time_close'].str.slice(stop=16))
    return df


def load_api_keys():
    if os.path.exists('apikeys.pkl'):
        with open('apikeys.pkl', 'rb') as keys:
            apikeys = pickle.load(keys)
    else:
        apikeys = [input('Wprowadź APIKEY: ').strip().upper()]

    return select_apikey(apikeys)


def select_apikey(apikeys):
    url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD'
    working_keys = []
    limited_keys = []
    for i in range(len(apikeys)):
        headers = {'X-CoinAPI-Key': apikeys[i]}
        response = rq.get(url, headers=headers)
        if response.status_code == 200:
            working_keys.append(apikeys[i])
        elif response == 429:
            limited_keys.append(apikeys[i])
    if len(working_keys) == 0:
        print("Podane klucze nie działają!")
        apikeys = [input('Wprowadź APIKEY (Jeśli chcesz zakończyć pracę programu wpisz \'q\': ').strip().upper()]
        if apikeys == 'Q':
            exit()
        else:
            select_apikey(apikeys)
    else:
        working_keys.extend(limited_keys)  # dodaj klucze, które wyczerpały limit na koniec
        with open('apikeys.pkl', 'wb') as file:
            pickle.dump(apikeys, file)
    return working_keys


def change_matrix(probability, alpha, change):
    neg_probab = 1 - probability
    for i in range(7):
        for j in range(24):
            if change[i, j] >= 0:
                change[i, j] = change[i, j] if probability[i, j] >= alpha else 0
            else:
                change[i, j] = change[i, j] if neg_probab[i, j] >= alpha else 0
    return change


def create_matrix(df):
    positive_ret = np.zeros((7, 24))
    quant = np.zeros_like(positive_ret)
    delta = np.zeros_like(positive_ret)
    for i in range(7):
        for j in range(24):
            temp = df[df['time_open'].dt.dayofweek == i]
            temp = temp[temp['time_open'].dt.hour == j]
            temp['change'] = round(temp['return'] / temp['price_open'] * 100, 2)
            delta[i][j] = temp['change'].mode() if len(temp['change'].mode()) == 1 else np.random.choice(
                temp['change'].mode())
            positive_ret[i][j] = sum(temp['return'].apply(lambda x: 1 if x > 0 else 0))
            quant[i][j] = temp.shape[0]

    return positive_ret, quant, delta


def predict(delta, prediction_data, last_values, alpha, resetrate, data):
    for idx, row in prediction_data.iterrows():
        if idx % resetrate == 0 and idx != 0:
            pos, a, delta = create_matrix(data)
            delta = change_matrix(pos / a, alpha, delta)
            if resetrate == 7:
                print('{}%'.format(int(idx * 100 / len(prediction_data.index))))
        day = prediction_data.iloc[[idx]]['time_open'].dt.weekday
        hour = prediction_data.iloc[[idx]]['time_open'].dt.hour
        new_price = last_values['price_close'] * delta[day, hour] / 100 + last_values[
            'price_close']
        prediction_data.loc[idx, 'price_close'] = new_price
        last_values = prediction_data.iloc[idx]

    return prediction_data
