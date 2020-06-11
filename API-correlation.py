import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def get_offers(url, currencies, Id):
    url += currencies[0] + currencies[1] + '/' + 'trades' + '.json?since=' + str(Id)
    response = requests.get(url).json()
    return response


def chart():
    currencies = ['BTC', 'USD']
    url = "https://bitbay.net/API/Public/"
    nr = 292759   #id of first operation in 2020. Set on this level to shorten download time.


    response = get_offers(url, currencies, Id=nr)
    last_id = response[-1]['tid']

    buys = []
    sells = []
    amount_buys = []
    amount_sells = []

    start = datetime.strptime(input("Podaj początek przedziału dat do badania korelacji (YYYY-MM-DD) (od 2020r): "),
                              '%Y-%m-%d')
    end = datetime.strptime(input("Podaj koniec przedziału dat do badania korelacji    (YYYY-MM-DD) (do dzisiaj): "),
                            '%Y-%m-%d')

    print('\nPobieranie danych...\n')

    while datetime.fromtimestamp(int(response[-1]['date'])) < end:
        response = get_offers(url, currencies, Id=last_id)

        for i in range(len(response)):

            if response[i]['type'] == 'buy' and start <= datetime.fromtimestamp(int(response[i]['date'])) <= end:
                buys.append(response[i]['price'])
                amount_buys.append(response[i]['amount'])

            elif response[i]['type'] == 'sell' and start <= datetime.fromtimestamp(int(response[i]['date'])) <= end:
                sells.append(response[i]['price'])
                amount_sells.append(response[i]['amount'])
        last_id = response[-1]['tid']

    correlation_coefficient_buys = np.corrcoef(buys, amount_buys)[1][0]
    correlation_coefficient_sells = np.corrcoef(sells, amount_sells)[1][0]

    info = '\nHigher value = higher correlation.\nValue from the range (-0.5; 0.5) in fact means no correlation'

    plt.subplot(1, 2, 1)
    plt.scatter(buys, amount_buys, color='blue', marker='X')
    plt.xticks(rotation=45)
    plt.xlabel('Buy Price [USD]')
    plt.ylabel('Amount')
    plt.title('Correlation coefficient =' + str(correlation_coefficient_buys) + str(info))

    plt.subplot(1, 2, 2)
    plt.scatter(sells, amount_sells, color='blue', marker='X')
    plt.xticks(rotation=45)
    plt.xlabel('Sell Price [USD]')
    plt.ylabel('Amount')
    plt.title('Correlation coefficient = ' + str(correlation_coefficient_sells) + str(info))

    fig = plt.gcf()
    fig.set_size_inches(36, 14)
    plt.savefig('correlation.png')
    plt.show()


chart()
