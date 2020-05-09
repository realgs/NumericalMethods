import pandas as pd
import requests


def show_wallet():
    wallet = pd.read_excel('WALLET.xlsx', index_col=0)
    print(wallet)


def add_currency():
    wallet = pd.read_excel('WALLET.xlsx', index_col=0)
    new = []
    cryptocurrency = (input('Podaj kryptowalutę: ')).upper()
    url = 'https://api.bitbay.net/rest/trading/orderbook/' + str(cryptocurrency) + '-' + 'USD'
    response = requests.get(url).json()

    while response['status'] == 'Fail':
        print('\nTaka kryptowaluta nie jest obsługiwana przez ten rynek.')
        cryptocurrency = (input('\nPodaj kryptowalutę jaką chcesz dodać: ')).upper()
        url = 'https://api.bitbay.net/rest/trading/orderbook/' + str(cryptocurrency) + '-' + 'USD'
        response = requests.get(url).json()
    amount = float(input('Podaj ilość: '))

    if cryptocurrency in wallet.values:
        wallet.loc[wallet['Currency'] == cryptocurrency, ['Amount']] += amount
    else:
        new.append([cryptocurrency, amount])
    decision = input('Chcesz coś jeszcze dodać do portfela? ')

    while decision.upper() == 'TAK':
        cryptocurrency = (input('Podaj kryptowalutę: ')).upper()
        url = 'https://api.bitbay.net/rest/trading/orderbook/' + str(cryptocurrency) + '-' + 'USD'
        response = requests.get(url).json()

        while response['status'] == 'Fail':
            print('\nTaka kryptowaluta nie jest obsługiwana przez ten rynek.')
            cryptocurrency = (input('\nPodaj walutę jaką chcesz dodać: ')).upper()
            url = 'https://api.bitbay.net/rest/trading/orderbook/' + str(cryptocurrency) + '-' + 'USD'
            response = requests.get(url).json()
        amount = float(input('Podaj ilość: '))

        if cryptocurrency in wallet.values:
            wallet.loc[wallet['Currency'] == cryptocurrency, ['Amount']] += amount
        else:
            new.append([cryptocurrency, amount])
        decision = input('Chcesz coś jeszcze dodać do portfela? ')

    update = pd.DataFrame(new, columns=wallet.columns)
    updated_wallet = wallet.append(update, ignore_index=True)
    updated_wallet.to_excel('WALLET.xlsx')

    return updated_wallet


def delete_currency():
    wallet = pd.read_excel('WALLET.xlsx', index_col=0)
    cryptocurrency = (input('Podaj Currency do usunięcia: ')).upper()

    while cryptocurrency not in wallet.values:
        cryptocurrency_or_end = (
            input('Nie posiadasz takiej waluty. Podaj Currency do usunięcia lub "koniec" aby zakończyć ')).upper()
        if cryptocurrency_or_end == 'KONIEC':
            break
    else:
        amount = float(input('Podaj ilość: '))
        index = wallet[wallet['Currency'] == cryptocurrency].index[0]
        wallet_amount = wallet.at[index, 'Amount']
        if amount >= wallet_amount:
            decision = input('Podałeś ilość taką jak/większą niż posiadasz. Chesz usunąć pełną ilość? ')
            if decision.upper() == 'TAK':
                delete_row = wallet[wallet['Currency'] == cryptocurrency].index
                wallet = wallet.drop(delete_row)
            else:
                amount = float(input('Podaj ponownie ilość: '))
                while amount > wallet_amount:
                    amount = float(input('Podaj ponownie ilość: '))
                wallet.loc[wallet['Currency'] == cryptocurrency, ['Amount']] -= amount
        else:
            wallet.loc[wallet['Currency'] == cryptocurrency, ['Amount']] -= amount
    wallet.to_excel('WALLET.xlsx')

    return wallet


def save_state(state):
    file = open("previous_result", 'w')
    file.write(str(state))
    file.close()


def read_previous_state():
    file = open("previous_result", 'r')
    line = file.readlines()
    previous_state = float(line[0])
    return previous_state


def get_rate(currency):
    if currency == 'PLN':
        rate = 1
    else:
        url = 'http://api.nbp.pl/api/exchangerates/tables/A/'
        response = requests.get(url).json()
        rates = response[0]['rates']
        rate_dict = list(filter(lambda c: c['code'] == str(currency), rates))
        rate = float(rate_dict[0]['mid'])

    return rate


def calculate():
    wallet = pd.read_excel('WALLET.xlsx', index_col=0)
    data = wallet.to_dict('records')
    currency = (input('\nPodaj walutę na jaką chcesz przeliczyć swój portfel: ')).upper()

    cryptocurrencies = []
    result = {}

    for dictionary in data:
        new_dictionary = {dictionary['Currency']: dictionary['Amount']}
        cryptocurrencies.append(new_dictionary)

    for dictionary in cryptocurrencies:
        cryptocurrency = list(dictionary.keys())[0]
        amount = list(dictionary.values())[0]
        url = 'https://api.bitbay.net/rest/trading/orderbook/' + str(cryptocurrency) + '-' + str(currency)
        response = requests.get(url).json()

        while response['status'] == 'Fail':
            print('\nTaka waluta nie jest obsługiwana przez ten rynek. Spróbuj ponownie:')
            currency = (input('\nPodaj skrót (np. USD) waluty na jaką chcesz przeliczyć swój portfel: ')).upper()
            url = 'https://api.bitbay.net/rest/trading/orderbook/' + str(cryptocurrency) + '-' + str(currency)
            response = requests.get(url).json()
        buys = response['buy']
        i, value = 0, 0

        if float(buys[i]['ca']) > amount:
            value += amount * float(buys[i]['ra'])
        else:
            while float(buys[i]['ca']) < amount and i < len(buys) - 1:
                value += float(buys[i]['ca']) * float(buys[i]['ra'])
                amount -= float(buys[i]['ca'])
                i += 1
            else:
                value += amount * float(buys[0]['ra'])
                if amount > float(buys[i]['ca']):
                    print('\nNie udało się sprzedać całej ilości ' + str(
                        cryptocurrency) + ', więc wynik to pewna estymacja\n')

        result.update({cryptocurrency: value})

    state = round(sum(result.values()), 2)
    print('Wartości poszczególnych obiektów w portfelu:\n', result)
    rate = get_rate(currency)
    state_to_save = round(float(state) * float(rate), 2)
    diff = state_to_save * 100 / read_previous_state() - 100
    print('\nPrzybliżona wartość portfela to: ', state, currency)
    if state_to_save - read_previous_state() > 0:
        print('Różnica w stosunku do poprzedniego stanu portfela to: +' + str(round(diff, 6)) + '%')
    else:
        print('Różnica w stosunku do poprzedniego stanu portfela to: ' + str(round(diff, 6)) + '%')
    save_state(state_to_save)


def main():
    question = '\nCo chcesz wykonać?\n1. Włożyć do portfela, 2. Usunąć z portfela, 3. Sprawdzić wartość portfela, ' \
               '4. Pokazać portfel, 0. Zakończyć\n '
    action = input(question)
    while not action.isnumeric():
        action = input('Podałeś nieobsługiwaną wartość, spójrz na dostępne opcje i spróbuj ponownie: ')

    action = int(action)
    while action != 0:
        if action == 1:
            add_currency()
            action = (int(input(question)))
        elif action == 2:
            delete_currency()
            action = (int(input(question)))
        elif action == 3:
            calculate()
            action = (int(input(question)))
        elif action == 4:
            show_wallet()
            action = (int(input(question)))
        else:
            action = (input('Wprowadziłeś wartość spoza przedziału {0, 1, 2, 3, 4}. Spróbuj ponownie: '))
            while not action.isnumeric():
                action = input('Podałeś nieobsługiwany format, spójrz na dostępne opcje i spróbuj ponownie: ')
            action = int(action)
    else:
        print('\nDziękuję za współpracę')


main()
