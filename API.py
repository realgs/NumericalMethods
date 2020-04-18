import requests
import matplotlib.pyplot as plt
import datetime
import numpy as np


def get_offers(url, currencies, to_console, category, Id):

    if category == 'trades':
        url += currencies[0]+currencies[1]+'/'+category+'.json?since='+str(Id)
    elif category == 'orderbook':
        url += currencies[0]+currencies[1]+'/'+category+'.json'
    response = requests.get(url).json()

    if to_console == True:
        print("\nOferty kupna oraz Ilości: \n", response['bids'])
        print("Oferty szprzedaży oraz Ilości: \n", response['asks'])

    return response

def chart():

    currencies = ['BTC', 'USD']
    url = "https://bitbay.net/API/Public/"
    nr = int(input('Podaj numer transakcji, od której chcesz rozpocząć wykres (mniejszy numer = więcej danych na wykresie): \nZaleca się min. 292759 (01.01.2020r.), gdyż mniejszy numer to dłuższy czas oczekiwania. Max numer: 303000\n'))
    response = get_offers(url, currencies, False, category='trades', Id=nr)

    buys = []
    sells = []
    date_buys = []
    date_sells = []

    last_id = response[-1]['tid']

    print('Pierwsza transakcja:', datetime.datetime.fromtimestamp(int(response[-1]['date'])).strftime('%Y-%m-%d %H:%M:%S'))
    print('\nPobieranie danych...\n')

    while len(response) == 50:
        response = get_offers(url, currencies, False, category='trades', Id=last_id)

        for i in range(len(response)):
            if response[i]['type'] == 'buy':
                buy = response[i]['price']
                buys.append(buy)
                date_buy = response[i]['date']
                date_buys.append(date_buy)
            else:
                sell = response[i]['price']
                sells.append(sell)
                date_sell = response[i]['date']
                date_sells.append(date_sell)
        last_id = response[-1]['tid']

    print('Ostatnia transakcja:', datetime.datetime.fromtimestamp(date_buys[-1]).strftime('%Y-%m-%d %H:%M:%S'))

    dif_b =[0]
    dift_b = [0]

    for i in range(len(date_buys) - 1):
        dif_b.append(buys[i + 1] - buys[i])
        if (date_buys[i + 1] - date_buys[i]) != 0:
            dift_b.append((buys[i + 1] - buys[i]) / (date_buys[i + 1] - date_buys[i]))
        else:
            dift_b.append(buys[i + 1] - buys[i])

    extr_buys = []
    extr_date_buys = []

    for i in range(len(date_buys) - 1):
        if dift_b[i] * dift_b[i+1] <= 0:
            extr_buys.append(buys[i])
            extr_date_buys.append(date_buys[i])

    dif_s = [0]
    dift_s = [0]

    for i in range(len(date_sells) - 1):
        dif_s.append(sells[i + 1] - sells[i])
        if (date_sells[i + 1] - date_sells[i]) != 0:
            dift_s.append((sells[i + 1] - sells[i]) / (date_sells[i + 1] - date_sells[i]))
        else:
            dift_s.append(sells[i + 1] - sells[i])

    extr_sells = []
    extr_date_sells = []

    for i in range(len(date_sells) - 1):
        if dift_s[i] * dift_s[i+1] <= 0:
            extr_sells.append(sells[i])
            extr_date_sells.append(date_sells[i])

    plt.subplot(1, 2, 1)
    plt.plot(date_buys, buys, color='blue', label='Price')
    plt.plot(date_buys, dif_b, color='red', label='Difference')
    plt.plot(date_buys, np.gradient(buys), color='black', label='Rate of change')
    plt.scatter(extr_date_buys, extr_buys, marker='x', color='red', label='Local extremum')
    plt.xlabel('Date [unix]')
    plt.ylabel('Price [USD]')
    plt.title('Buy USD-BTC')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(date_sells, sells, color='blue', label='Price')
    plt.plot(date_sells, dif_s, color='red', label='Difference')
    plt.plot(date_sells, np.gradient(sells), color='black', label='Rate of change')
    plt.scatter(extr_date_sells, extr_sells, marker='x', color='red', label='Local extremum')
    plt.xlabel('Date [unix]')
    plt.ylabel('Price [USD]')
    plt.title('Sell USD-BTC')
    plt.legend()

    fig = plt.gcf()
    fig.set_size_inches(36, 14)
    plt.show()

chart()