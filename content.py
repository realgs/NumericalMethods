import requests as rq
import pandas as pd
import os
import pickle


def download_markets(apikeys=None):
    if not apikeys and os.path.exists('apikeys.pkl'):
        with open('apikeys.pkl', 'rb') as f:
            apikeys = pickle.load(f)
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
        return pd.DataFrame(response), apikeys
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
            markets = markets.append(currency(dataframe, base='USD', quote=quote),sort=True)
            return markets
        else:
            print("Nie można zamienić")
            return 0


def bids(markets):
    pass


if not os.path.exists('markets.json'):
    response = download_markets()
else:
    response = pd.read_json(r'markets.json', orient='records')
print(currency_check(response, base='TUSD', quote='PLN')[['symbol_id', 'asset_id_base', 'asset_id_quote']])
# print(response['asset_id_quote'].unique().shape)
