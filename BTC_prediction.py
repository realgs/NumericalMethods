import requests
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def get_50_transactions(id):
    url = "https://bitbay.net/API/Public/BTCUSD/trades.json?since=" + str(id)
    response = requests.get(url).json()
    transactions = pd.DataFrame(response)
    return transactions


def complete_data():
    start_id = 292759   #id of first operation in 2020. Set on this level to shorten download time.
    print('\nPobieram dane ... (ok. 2 minuty)')
    first_data_part = get_50_transactions(id=start_id)
    last_id = first_data_part['tid'].iloc[-1]

    while get_50_transactions(last_id).shape[0] == 50:
        data_part = get_50_transactions(id=last_id)
        first_data_part = first_data_part.append(data_part, ignore_index=True)
        last_id = first_data_part['tid'].iloc[-1]

    last_data_part = get_50_transactions(id=last_id)
    data = first_data_part.append(last_data_part, ignore_index=True)
    data = data.drop(columns=['amount', 'type', 'tid'])
    data['date'] = pd.to_datetime(data['date'], unit='s')
    print('\nPobieranie zakończone.')

    return data


def final_data():
    data = complete_data()
    data = data[data['date'] > start]
    columns = data.columns.difference(['date'])
    data[columns] = data[columns].astype(float)
    data_daily = data.resample('d', on='date').mean().dropna(how='all')
    change = data_daily['price'].pct_change().fillna(0)
    data_daily = data_daily.assign(change=change.values).reset_index()
    data_daily['day of week'] = data_daily['date'].dt.day_name()

    return data_daily


def day_probability(day_name, data):
    daily_data = data.loc[data['day of week'] == day_name]
    day_changes = daily_data['change'].to_numpy()
    decreases_amount = np.sum(day_changes < 0)
    increases_amount = np.sum(day_changes > 0)
    all_changes = data['change'].to_numpy()
    increases = all_changes[all_changes > 0]
    decreases = all_changes[all_changes < 0]

    if decreases_amount > increases_amount:
        pick = np.random.choice(decreases)
    elif increases_amount > decreases_amount:
        pick = np.random.choice(increases)
    else:
        pick = np.random.choice(all_changes)

    return pick


def generate_dates(data):
    dates_to_predict = []
    days_to_predict = []

    for i in range(1, 8):
        date = data.iloc[-1]['date'] + datetime.timedelta(days=i)
        day = date.strftime('%A')
        dates_to_predict.append(date)
        days_to_predict.append(day)

    return dates_to_predict, days_to_predict


def prediction(data):
    days = generate_dates(data)[1]
    changes = []
    for day in days:
        changes.append(day_probability(day, data))

    last_price = data.iloc[-1]['price']
    predicted_prices = [0] * len(changes)
    for i in range(len(changes)):
        predicted_prices[i] = last_price + changes[i]*last_price
        last_price = predicted_prices[i]

    predicted_prices.insert(0, data.iloc[-1]['price'])
    predicted_dates = generate_dates(data)[0]
    predicted_dates.insert(0, data.iloc[-1]['date'])

    return predicted_dates, predicted_prices


def user_input():
    while True:
        try:
            inp = input("Podaj datę początkową badania yyyy-mm-dd (tylko 2020 r. i zalecana > 2tyg wstecz): ")
            start = datetime.datetime.strptime(inp, "%Y-%m-%d")
            while start < datetime.datetime.strptime('2020-01-01', '%Y-%m-%d') or start > datetime.datetime.today():
                print('Wprowadziłeś datę spoza zakresu!')
                while True:
                    try:
                        inp = input("Podaj datę początkową badania yyyy-mm-dd (tylko 2020 r. i zalecana > 2tyg wstecz): ")
                        start = datetime.datetime.strptime(inp, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Wprowadziłeś zły format!")
            break
        except ValueError:
            print("Wprowadziłeś zły format!")

    return start


def main():
    data = final_data()
    print('\nTworzę wykres...')

    predictions = []
    for i in range(100):
        plt.plot(prediction(data)[0], prediction(data)[1], 'lightskyblue')
        predictions.append(prediction(data)[1])

    predictions_arr = np.array(predictions)
    average_prediction = np.mean(predictions_arr, axis=0)
    plt.plot(prediction(data)[0], average_prediction, 'blue')
    plt.plot(data['date'], data['price'], 'blue')

    if data['date'].shape[0] > 21:
        decision = (input('\nChcesz obejrzeć tylko fragment wykresu, aby lepiej widzieć predykcję? (tak/nie): '))
        if decision.upper() == 'TAK':
            plt.xlim([datetime.date.today() - datetime.timedelta(days=14), datetime.datetime.today() + datetime.timedelta(days=7)])
        else:
            plt.xlim(data.iloc[0]['date'], datetime.date.today() + datetime.timedelta(days=7))
    else:
        plt.xlim(data.iloc[0]['date'], datetime.date.today() + datetime.timedelta(days=7))

    print('\nStatystyki symulacji:')
    print('Średnia: ', np.mean(average_prediction))
    print('Mediana:', np.median(average_prediction))
    print('Odchylenie standardowe:', np.std(average_prediction))

    plt.xlabel('Date')
    plt.ylabel('Price [USD]')
    plt.title('BTC price with 7-days prediction')
    fig = plt.gcf()
    fig.set_size_inches(36, 14)
    plt.show()


start = user_input()
main()
