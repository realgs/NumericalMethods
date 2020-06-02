import requests
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_data(crypto):
    now_from = 1588291200
    now_to = time.time()
    past_to = 1559260800
    past_from = past_to - (now_to - now_from)
    past_crypto = requests.get(
        "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_{}&start={}&end={}&period=14400".format(
            crypto, past_from, past_to))
    now_crypto = requests.get(
        "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_{}&start={}&end={}&period=14400".format(
            crypto, now_from, now_to))
    return past_crypto.json(), now_crypto.json()


def to_period(period):
    prices = []
    for item in period:
        prices.append(item['close'])
    return prices


def hist_pred(data):
    window_size = 3
    numbers_series = pd.Series(data)
    train = [numbers_series[i] for i in range(window_size)]
    test = [numbers_series[i] for i in range(window_size, len(numbers_series))]
    predictions = list()

    for j in range(len(test)):
        length = len(train)
        mean = np.mean([train[i] for i in range(length - window_size, length)])
        obs = test[j]
        predictions.append(mean)
        train.append(obs)

    return predictions


def plots(price, prediction, title):
    plt.figure(figsize=(15, 5))
    plt.plot(price, label="Crypto")
    plt.plot(prediction, label='Simulation')
    plt.legend()
    plt.title(title, fontsize=24)
    plt.show()


name = input("Choose your crypto (ETC, DASH, XMR): ").upper()

if name in ["ETC", "DASH", "XMR"]:
    print("The time period is from beginning of the month till today.\n"
          "And the same amount of days exactly one year ago.")

    past, present = get_data(name)

    past_price = to_period(past)
    present_price = to_period(present)

    prediction = hist_pred(past_price)

    predict_future = hist_pred(prediction)

    plots(past_price, prediction, "PAST")
    plots(present_price, predict_future, "FUTURE")

else:
    print("Wrong input")
