import numpy as np
import requests
import matplotlib.pyplot as plt


def plots():
    response = requests.get("https://bitbay.net/API/Public/BTC/trades.json?sort=asc")
    data = response.json()

    print(data)

    list_of_prices = []
    list_of_extremes = []
    list_of_indexes = []

    time = np.array(np.arange(0, 50))

    for i in range(len(data)):
        price = data[i]['price']
        list_of_prices.append(price)

    list_of_prices = np.array(list_of_prices)

    for j in range(len(list_of_prices)):
        if (list_of_prices[j] - list_of_prices[j - 1]) != 0 or (list_of_prices[j] - list_of_prices[j + 1]) != 0:
            list_of_extremes.append(list_of_prices[j])
            list_of_indexes.append(j)

    list_of_extremes = np.array(list_of_extremes)
    list_of_indexes = np.array(list_of_indexes)

    plt.plot(time, list_of_prices, label='Price plot')
    plt.plot(list_of_indexes, list_of_extremes, 'ro', markersize=2)

    plt.xlabel('Time')
    plt.ylabel('Prices')

    plt.title('Price plot')

    plt.legend()

    plt.show()


plots()
