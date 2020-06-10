import numpy as np
import requests
import matplotlib.pyplot as plt
import datetime


def plots():
    response = requests.get("https://bitbay.net/API/Public/BTC/trades.json?sort=asc")
    data = response.json()

    list_of_prices = []
    list_of_dates = []
    list_of_extremes = []
    list_of_indexes = []

    for i in range(len(data)):
        price = data[i]['price']
        list_of_prices.append(price)
        date = datetime.datetime.fromtimestamp(data[i]['date']).strftime('%H:%M:%S')
        list_of_dates.append(date)

    list_of_prices = np.array(list_of_prices)
    list_of_dates = np.array(list_of_dates)

    for j in range(len(list_of_prices)):
        if (list_of_prices[j] - list_of_prices[j - 1]) != 0 or (list_of_prices[j] - list_of_prices[j + 1]) != 0:
            list_of_extremes.append(list_of_prices[j])
            list_of_indexes.append(j)

    list_of_extremes = np.array(list_of_extremes)
    list_of_indexes = np.array(list_of_indexes)

    plt.plot(list_of_dates, list_of_prices, label='Price plot')
    plt.plot(list_of_indexes, list_of_extremes, 'ro', markersize=2)

    plt.xlabel('Time')
    plt.ylabel('Prices')

    plt.xticks(rotation=90, fontsize=9)

    plt.title('Price plot')

    plt.legend()

    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')

    plt.show()


plots()
