import requests as rq
import pandas as pd
import os
import pickle
import json


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
    elif quote not in dataframe['asset_id_quote'].unique():
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


def save_apikey(apikeys):
    with open('apikeys.pkl', 'wb') as f:
        pickle.dump(apikeys, f)
        return apikeys


def download_orderbook(markets):
    apikeys = load_apikeys()
    limit = 100
    columns = ['symbol_id', 'type', 'price', 'size', 'from', 'to']
    orderbook = pd.DataFrame(columns=columns)
    url = 'https://rest.coinapi.io/v1/orderbooks/{}/current?limit_levels={}&apikey={}'
    for index, row in markets[['symbol_id', 'asset_id_base', 'asset_id_quote']].iterrows():
        response = rq.get(url.format(row['symbol_id'], limit, apikeys[0]))
        if response.status_code == 429:
            print("Klucz się wyczerpał")
            apikeys.append(apikeys.pop(0))
            with open('apikeys.pkl', 'wb') as f:
                pickle.dump(apikeys, f)
            download_orderbook(markets)
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
            orderbook = orderbook.append(df, ignore_index=True)
    orderbook[['price', 'size']] = orderbook[['price', 'size']].astype('float64')
    return orderbook


def exchange(df, currentsize, currentprice=0, markets_list=[], base='', quote=''):
    df = df[df['size'] <= currentsize].reset_index(drop=True)
    if currentsize == 0 or len(df.index) == 0:
        if len(df.index) == 0:
            currentprice, currentsize, markets_list = estimate(currentprice, currentsize, base, quote, markets_list)
        return currentprice, currentsize, markets_list
    accuracy = df['size'].min()
    if currentsize < accuracy:
        currentprice, currentsize, markets_list = estimate(currentprice, currentsize, base, quote, markets_list)
        return currentprice, currentsize, markets_list
    argmax = df['price'].idxmax()
    maximum = df.loc[argmax, :]
    df = df.drop(df.index[argmax]).reset_index(drop=True)
    print(maximum)
    currentprice += maximum['price'] * maximum['size']
    currentsize -= maximum['size']
    markets_list.append(maximum['symbol_id'][:maximum['symbol_id'].find('_')])
    return exchange(df, currentsize, currentprice, markets_list)


def estimate(price, size, base, quote, market_lists):
    apikeys = load_apikeys()
    url = 'https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}'.format(base, quote, apikeys[0])
    response = rq.get(url)
    if response.status_code == 429:
        print("Klucz się wyczerpał")
        apikeys.append(apikeys.pop(0))
        with open('apikeys.pkl', 'wb') as f:
            pickle.dump(apikeys, f)
        estimate(price, size, base, quote)
    elif response.status_code == 200:
        response = response.json()
        price += response['rate'] * size
        market_lists.append("Estimation")
    return price, 0, market_lists


def load_markets():
    if not os.path.exists('markets.json'):
        response = download_markets()
    else:
        response = pd.read_json(r'markets.json', orient='records')
    return response


def load_user_data():
    if os.path.exists('user.json'):
        with open('user.json', 'r') as f:
            user = json.load(f)
        return user
    else:
        return 0


def wyb1(user):
    user['']
    pass


def wyb2():
    pass


def wyb3():
    pass


def wyb4():
    apikeys = load_apikeys()
    newkey = input("Wprowadź nowy klucz do coinAPI.io: ")
    url = 'https://rest.coinapi.io/v1/exchangerate/USD/BTC?apikey={}'.format(newkey)
    if rq.get(url).status_code == 200:
        if apikeys:
            apikeys.append(newkey)
        else:
            apikeys = [newkey]
        save_apikey(apikeys)
        print("Pomyślnie dodano klucz!")
        return 0
    elif rq.get(url).status_code == 429:
        print("Klucz się wyczerpał, wprowadź nowy!")
        if apikeys:
            apikeys.append(newkey)
        else:
            apikeys = [newkey]
        save_apikey(apikeys)
        wyb4()
    else:
        print("Wprowadzono błędny klucz!")
        confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
        if confirm == 'q':
            return 0
        else:
            wyb4()


def wyb5():
    msg = 'Wprowadź numer klucza, który chcesz usunąć, dla usunięcia całej bazy wprowadź "a": '
    apikeys = load_apikeys()
    if apikeys:
        for i in range(len(apikeys)):
            print('{}. {}'.format(i + 1, apikeys[i]))
        answer = input(msg)
        if answer.lower() == 'a':
            os.remove('apikeys.pkl')
            print('Plik usunięty!')
        else:
            try:
                answer = int(answer)
            except ValueError:
                print("Błędny input!")
                confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
                if confirm == 'q':
                    return 0
                else:
                    wyb5()
            if 1 < answer > len(apikeys):
                print("Nie istnieje taki wiersz!")
                confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
                if confirm == 'q':
                    return 0
                else:
                    wyb5()
            else:
                del apikeys[answer - 1]
                save_apikey(apikeys)
                print("Usnięto {}. wiersz!".format(answer))
                return 0


def wyb6():
    print('Uaktualniam listę możliwych marketów... Może to chwile potrwać..')
    return download_markets()


def wyb7():
    pass


def save_user_data():
    pass


def main():
    response = load_markets()
    base = 'BTC'
    quote = 'USD'
    amount = 13.2837204820

    markets = currency_check(response[response['symbol_type'] == 'SPOT'], base=base, quote=quote)
    # print(markets)
    if len(markets.index) > 30:
        orderbook = download_orderbook(markets.sample(30))
    else:
        orderbook = download_orderbook(markets)

    bids = orderbook[orderbook['type'] == 'bid'].reset_index(drop=True)
    # if len(bids.index) == 0:

    # print(bids)
    print(exchange(bids, amount, base=base, quote=quote))
    # print(response['asset_id_quote'].unique().shape)

main()