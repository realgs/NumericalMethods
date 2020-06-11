import requests as rq
import pandas as pd
import os
import pickle


def show(user):
    print()
    if type(user) == int:
        user = load_user_data()
        if type(user) == int:
            print("Baza jest pusta")
            return 0
    newUser = user[['base', 'quote', 'size', 'current_val', 'init_val', 'now']]
    col = {'base': 'Wal. bazowa', 'quote': 'Wal. docelowa', 'size': 'Ilość', 'now': 'Zysk',
           'init_val': 'Zapłacono', 'current_val': 'Obecna wartość'}
    with pd.option_context('display.max_rows', None, 'display.max_columns', 6):
        print(newUser.rename(columns=col))


def check_api(apikeys):
    url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD?apikey={}'
    flag = False
    apikeys = [apikeys] if type(apikeys) != list else apikeys
    for key in apikeys:
        status = rq.get(url.format(key)).status_code
        if status == 200:
            flag = True
            break
    return flag


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
        if not check_api(apikeys):
            key = input("Podaj prawidłowy klucz: ")
            while not check_api(key):
                key = input("Podaj prawidłowy klucz: ")
            apikeys.extend(key)
            apikeys = save_apikey(apikeys)
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
        return 1
    else:
        markets = currency(dataframe, base)
    if quote in markets['asset_id_quote'].unique():
        return currency(markets, quote=quote)
    elif quote not in markets['asset_id_quote'].unique():
        print('Aby zamienić na twoją walutę docelową będzie potrzeba przewalutowania')
        if 'USD' in markets['asset_id_quote'].unique():
            markets = currency(markets, quote='USD')
            return markets
        else:
            print("Nie można zamienić")
            return 1


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
            if not check_api(apikeys):
                key = input("Podaj prawidłowy klucz: ")
                while not check_api(key):
                    key = input("Podaj prawidłowy klucz: ")
                apikeys.extend(key)
                apikeys = save_apikey(apikeys)
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
    currentprice += maximum['price'] * maximum['size']
    currentsize -= maximum['size']
    markets_list.append(maximum['symbol_id'][:maximum['symbol_id'].find('_')])
    return exchange(df, currentsize, currentprice, markets_list)


def estimate(price, size, base, quote, market_lists):
    apikeys = load_apikeys()
    url = 'https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}'.format(base, quote, apikeys[0])
    response = rq.get(url)
    if response.status_code == 429:
        if not check_api(apikeys):
            key = input("Podaj prawidłowy klucz: ")
            while not check_api(key):
                key = input("Podaj prawidłowy klucz: ")
            apikeys.extend(key)
            apikeys = save_apikey(apikeys)
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


def estimate_foreign(size, base, quote, market_lists=[]):
    apikeys = load_apikeys()
    url = 'https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}'.format(base, quote, apikeys[0])
    response = rq.get(url)
    if response.status_code == 429:
        if not check_api(apikeys):
            key = input("Podaj prawidłowy klucz: ")
            while not check_api(key):
                key = input("Podaj prawidłowy klucz: ")
            apikeys.extend(key)
            apikeys = save_apikey(apikeys)
        print("Klucz się wyczerpał")
        apikeys.append(apikeys.pop(0))
        with open('apikeys.pkl', 'wb') as f:
            pickle.dump(apikeys, f)
        estimate_foreign(size, base, quote)
    elif response.status_code == 200:
        response = response.json()
        price = response['rate'] * size
        return price, market_lists


def load_markets():
    if not os.path.exists('markets.json'):
        response = download_markets()
    else:
        response = pd.read_json(r'markets.json', orient='records')
    return response[response['symbol_type'] == 'SPOT']


def load_user_data():
    if os.path.exists('user.json'):
        user = pd.read_json(r'user.json', orient='records')
        return user
    else:
        return 0


def save_user(user):
    user.to_json(r'user.json', orient='records')
    print("Zapisano dane użytkownika")
    return user


def wyb1(user, response):
    temp = {}
    temp['base'] = [input("Wprowadź kod waluty bazowej (np.BTC): ")]
    temp['quote'] = [input("Wprowadź kod waluty docelowej (np.PLN): ")]
    markets = currency_check(response, temp['base'][0], temp['quote'][0])
    if type(markets) == int:
        print("Wprowadzono nieprawidłową liczbę!")
        confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
        if confirm == 'q':
            return user
        else:
            wyb1(user, response)
    temp['size'] = input("Wprowadź ilość waluty: ")
    try:
        temp['size'] = [float(temp['size'])]
    except ValueError:
        print("Wprowadzono nieprawidłową liczbę!")
        confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
        if confirm == 'q':
            return user
        else:
            wyb1(user, response)
    print("Trwa analiza najdroższej wyceny...")
    if len(markets.index) > 10:
        orderbook = download_orderbook(markets.sample(10))
    else:
        orderbook = download_orderbook(markets)
    bids = orderbook[orderbook['type'] == 'bid'].reset_index(drop=True)
    temp['current_val'], _, temp['market_l'] = exchange(bids, temp['size'][0], base=temp['base'][0],
                                                        quote=bids['to'][0])
    if bids['to'][0] != temp['quote'][0]:
        temp['current_val'], temp['market_l'] = estimate_foreign(temp['size'][0], bids['to'][0], temp['quote'][0],
                                                                 temp['market_l'])
    temp['init_val'] = input("Podaj wartość początkową (przy zakupie): ")
    try:
        temp['init_val'] = [float(temp['init_val'])]
    except ValueError:
        print("Wprowadzono nieprawidłowy typ danych!")
        confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
        if confirm == 'q':
            return user
        else:
            wyb1(user, response)
    temp['current_val'] = [temp['current_val']]
    temp['now'] = [temp['current_val'][0] - temp['init_val'][0]]
    temp['market_l'] = [temp['market_l']]
    temp_df = pd.DataFrame.from_dict(temp)
    temp_df['size'] = temp_df['size'].astype('float64')
    if type(user) == int:
        save_user(temp_df)
        return temp_df
    else:
        user = user.append(temp_df, ignore_index=True)
        user['size'] = user['size'].astype('float64')
        save_user(user)
    return user


def wyb2(user):
    if type(user) == int:
        print("Baza pusta!")
        user = load_user_data()
        if type(user) == int:
            return 0
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(user[['base', 'quote', 'size', 'init_val']])
    answer = input("Podaj index który chcesz edytować, jeśli chcesz przejść do trybu usuwania wierszy wprowadź 'e':")
    if answer == 'e':
        delete = input("Podaj index, który chcesz trwale usunąć:")
        try:
            delete = int(delete)
        except ValueError:
            print("Błędny input!")
            confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
            if confirm == 'q':
                return user
            else:
                wyb2(user)
        if delete < 0 or delete > len(user.index) - 1:
            print("Wprowadzono błędny index")
            confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
            if confirm == 'q':
                return user
            else:
                wyb2(user)
        elif delete == 0 and len(user.index) == 1:
            os.remove('apikeys.pkl')
            print('Plik usunięty!')
            return 0
        else:
            user = user.drop(user.index[delete])
            save_user(user)
            return user
    else:
        try:
            row = int(answer)
        except ValueError:
            print("Błędny input!")
            confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
            if confirm == 'q':
                return user
            else:
                wyb2(user)
        if row < 0 or row > len(user.index) - 1:
            print("Wprowadzono błędny index")
            confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
            if confirm == 'q':
                return user
            else:
                wyb2(user)
        else:
            column = input("Podaj nazwę kolumny, której wartość chesz edytować 'size','init_val' : ")
            if column in ['size', 'init_val']:
                type_b = user[column].dtype
                user.loc[row, column] = input("Wprowadź wartość w takiej samej formie jaka była!: ")
                try:
                    user[column] = user[column].astype(type_b)
                except ValueError:
                    print("Wprowadzono nie prawidłowy typ danych!")
                    confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
                    if confirm == 'q':
                        return user
                    else:
                        wyb2(user)
                save_user(user)
                response = load_markets()
                print("Uaktualniam bazę danych...")
                wyb3(user, response)
                return user
            else:
                print("Podanej kolumny nie można edytować!")
                print("Wprowadzono nie prawidłowy typ danych!")
                confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
                if confirm == 'q':
                    return user
                else:
                    wyb2(user)


def wyb3(user, response):
    if type(user) == int:
        print("Baza pusta!")
        user = load_user_data()
        if type(user) == int:
            return 0
    for index, row in user.iterrows():
        base = row['base']
        quote = row['quote']
        size = row['size']
        markets = currency_check(response, base, quote)
        if len(markets.index) > 5:
            orderbook = download_orderbook(markets.sample(5))
        else:
            orderbook = download_orderbook(markets)
        bids = orderbook[orderbook['type'] == 'bid'].reset_index(drop=True)
        current_val, _, market_l = exchange(bids, size, base=base, quote=quote)
        if bids['to'][0] != quote:
            current_val, market_l = estimate_foreign(size, bids['to'][0], quote, market_l)
        now = current_val - row['init_val']
        user.loc[index, 'current_val'] = current_val
        user.loc[index, 'now'] = now
    user = save_user(user)
    return user


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
            if 1 > answer or answer > len(apikeys):
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


def wyb7(user, response):
    if type(user) == int:
        user = load_user_data()
        if type(user) == int:
            print("Baza pusta!")
    primary_quote = input("Wprowadź walutę docelową (np.PLN): ")
    if primary_quote not in response['asset_id_quote'].unique():
        if primary_quote not in response['asset_id_base'].unique():
            print("Waluta nieobsługiwalna!")
            confirm = input("Jeśli chcesz wrócić do menu wprowadź 'q'")
            if confirm == 'q':
                return 0
            else:
                wyb7(user, response)
    value = 0
    paid = 0
    for index, row in user.iterrows():
        base = row['base']
        quote = row['quote']
        size = row['size']
        current_val = row['current_val']
        init_val = row['init_val']
        if quote == primary_quote:
            value += current_val
            paid += init_val
            continue
        else:
            current_val, _ = estimate_foreign(current_val, quote, primary_quote)
            init_val, _ = estimate_foreign(init_val, quote, primary_quote)
            value += current_val
            paid += init_val
    return value, paid, primary_quote
