import requests as rq
import pandas as pd
import os
import pickle


def download_markets(apikeys=None):
    if not apikeys and os.path.exists('apikeys.pkl'):
        apikeys = load_apikeys()
    elif not apikeys and not os.path.exists('apikeys.pkl'):
        print('Nie wykryto pliku apikeys.pkl!')
        apikeys = [input("Podaj swój klucz API:")]
        response = rq.get('https://rest.coinapi.io/v1/symbols?apikey={}'.format(apikeys[0]))
        if response.status_code != 200:
            print("Niepoprawny klucz!")
            download_markets()
        else:
            response = pd.DataFrame(response.json())
            with open('apikeys.pkl', 'wb') as f:
                pickle.dump(apikeys, f)
            response.to_json(r'markets.json', orient='records')
            return response, apikeys
    url = 'https://rest.coinapi.io/v1/symbols?apikey={}'.format(apikeys[0])
    try:
        response = pd.DataFrame(rq.get(url).json())
        response.to_json(r'markets.json', orient='records')
        return pd.DataFrame(response)
    except ValueError:
        if len(apikeys) > 1:
            apikeys.append(apikeys.pop(0))
            print("Zmiana klucza (obecny osiągnął limit)...")
            download_markets(apikeys)
        else:
            print("Klucz wyczerpał limit, podaj nowy klucz!")
            while True:
                apikey = input("Wrowadź klucz: ")
                response = rq.get('https://rest.coinapi.io/v1/symbols?apikey={}'.format(apikey)).json()
                if response.status_code != 200 and apikey in apikeys:
                    print("Niepoprawny klucz!")
                else:
                    apikeys.insert(0, apikey)
                    with open('apikeys.pkl', 'wb') as f:
                        pickle.dump(apikeys, f)
                    break
            download_markets(apikeys)


def currency(dataframe, base=None, quote=None):
    if base and quote:
        curr_market = dataframe[dataframe['asset_id_base'] == base]
        curr_market = curr_market[curr_market['asset_id_quote'] == quote]
    elif base:
        curr_market = dataframe[dataframe['asset_id_base'] == base]
    elif quote:
        curr_market = dataframe[dataframe['asset_id_quote'] == quote]
    return curr_market.reset_index()


def currency_check(dataframe, base, quote):
    if base not in dataframe['asset_id_base'].unique():
        print("Nie ma takiej waluty bazowej!")
        return 0
    if quote not in dataframe['asset_id_quote'].unique():
        print("Nie ma takiej waluty na którą chcesz wymienić w bazie!")
        return 0
    else:
        markets = currency(dataframe, base)
    if quote in markets['asset_id_quote'].unique():
        return currency(markets, quote=quote)
    elif quote not in markets['asset_id_quote'].unique():
        print('Aby zamienić na twoją walutę docelową będzie potrzeba przewalutowania')
        if 'USD' in markets['asset_id_quote'].unique():
            markets = currency(markets, quote='USD')
            # markets = markets.append(currency(dataframe, base='USD', quote=quote), sort=True)
            return markets
        else:
            print("Nie można zamienić")
            return 0


def load_apikeys():
    if os.path.exists('apikeys.pkl'):
        with open('apikeys.pkl', 'rb') as f:
            apikeys = pickle.load(f)
        return apikeys
    else:
        return 0


def download_bids(markets):
    apikeys = load_apikeys()
    limit = 10000
    columns = ['symbol_id', 'type', 'price', 'size', 'from', 'to']
    bids = pd.DataFrame(columns=columns)
    url = 'https://rest.coinapi.io/v1/orderbooks/{}/current?limit_levels={}&apikey=3C0B0442-9998-494F-8292-36A1961DBCCB'
    for index, row in markets[['symbol_id', 'asset_id_base', 'asset_id_quote']].iterrows():
        response = rq.get(url.format(row['symbol_id'], limit))
        if response.status_code == 429:
            print("Klucz się wyczerpał")
            apikeys.append(apikeys.pop(0))
            download_bids(markets)
        if response.status_code == 200:
            response = response.json()
            ToDataFrame = {}
            length = len(response['asks']) + len(response['bids'])
            temp_id = [response['symbol_id']] * length
            temp_type = ['ask'] * len(response['asks'])
            temp_type1 = ['bid'] * len(response['bids'])
            temp_type.extend(temp_type1)
            temp_from = [row['asset_id_base']] * length
            temp_to = [row['asset_id_quote']] * length
            temp_price = []
            temp_size = []
            for ask in response['asks']:
                temp_price.append(ask['price'])
                temp_size.append(ask['size'])
            for bid in response['bids']:
                temp_price.append(bid['price'])
                temp_size.append(bid['size'])
            ToDataFrame['symbol_id'] = temp_id
            ToDataFrame['type'] = temp_type
            ToDataFrame['price'] = temp_price
            ToDataFrame['size'] = temp_size
            ToDataFrame['from'] = temp_from
            ToDataFrame['to'] = temp_to
            df = pd.DataFrame.from_dict(ToDataFrame, orient='index').transpose()
            bids = bids.append(df, ignore_index=True)
    return bids


if not os.path.exists('markets.json'):
    response = download_markets()
else:
    response = pd.read_json(r'markets.json', orient='records')
markets = currency_check(response, base='TUSD', quote='PLN')[['symbol_id', 'asset_id_base', 'asset_id_quote']]
print(markets)
download_bids(markets)
# print(response['asset_id_quote'].unique().shape)
