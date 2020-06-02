import requests
import datetime
import time
import statistics
import pandas as pd
import matplotlib.pyplot as plt


def get_data(crypto):
    now = time.time()
    date = input("Enter date (YYYY-MM-DD): ")
    date_timestamp = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
    crypto = requests.get(
        "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_{}&start={}&end={}&period=14400".format(
            crypto, date_timestamp, now))
    return crypto.json()


def model(crypto):
    prices = []

    for item in crypto:
        prices.append(item['close'])

    window_size = 3
    numbers_series = pd.Series(prices)
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()

    size = int(len(prices) * 0.6)

    plt.figure(figsize=(15, 5))
    plt.plot(prices[:size], label='Crypto')
    plt.plot(moving_averages[size:], label='Simulation')
    plt.legend()
    plt.title("Prediction")
    plt.show()


def stats(crypto):
    prices = []
    list_of_growths = []
    list_of_declines = []

    for item in crypto:
        prices.append(item['close'])

    for i in range(len(prices) - 1):
        if prices[i] > prices[i + 1]:
            list_of_declines.append(prices[i])
        elif prices[i] < prices[i + 1]:
            list_of_growths.append(prices[i])

    growth_mean = statistics.mean(list_of_growths)
    decline_mean = statistics.mean(list_of_declines)

    growth_median = statistics.median(list_of_growths)
    decline_median = statistics.median(list_of_declines)

    st_dev_growth = statistics.stdev(list_of_growths)
    st_dev_decline = statistics.stdev(list_of_declines)

    print("Statistics for inclines and declines respectively:\n"
          "Means: {}, {}\n"
          "Medians: {}, {}\n"
          "Standard deviation: {}, {}".format(growth_mean, decline_mean,
                                              growth_median, decline_median,
                                              st_dev_growth, st_dev_decline))


name = input("Choose your crypto (ETC, DASH, XMR): ").upper()

if name in ["ETC", "DASH", "XMR"]:
    crypto = get_data(name)
    model(crypto)
    stats(crypto)
else:
    print("Wrong input")
