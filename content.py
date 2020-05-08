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


def currency(dataframe, base, quote):
    curr_market = dataframe[dataframe['asset_id_base'] == base]
    curr_market = curr_market[curr_market['asset_id_quote'] == quote]
    return curr_market

#
# if not os.path.exists('markets.json'):
#     response = download_markets()
# else:
#     response = pd.read_json(r'markets.json', orient='records')
# response.to_msgpack('responses.msg')
# print(response['asset_id_base'].unique().shape)
# print(response['asset_id_quote'].unique().shape)
download_markets()
