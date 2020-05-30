import requests
import time
import matplotlib.pyplot as plt
import pandas as pd


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


def moving_avg(data):
    window_size = 15
    numbers_series = pd.Series(data)
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()

    moving_averages_list = moving_averages.tolist()
    without_nans = moving_averages_list[window_size - 1:]

    return without_nans


def sim(price):
    size = 100
    simulated = []

    for i in range(size):
        simulation_data = moving_avg(price)
        simulated.append(simulation_data)

    result = []

    for i in range(len(simulated[0])):
        values = []

        for j in range(len(simulated)):
            values.append(simulated[j][i])

        average = sum(values) / len(values)
        result.append(average)

    return result


def plots(price, one, avg, title):
    plt.figure(figsize=(18, 8))
    plt.subplot(2, 2, 1)
    plt.plot(price, '-m')
    plt.title("Price")
    plt.subplot(2, 2, 2)
    plt.plot(one, '-g')
    plt.title("One simulation")
    plt.subplot(2, 2, 3)
    plt.plot(avg, '-b')
    plt.title("Avg simulation")
    plt.suptitle(title, fontsize=26)
    plt.show()


name = input("Choose your crypto (ETC, DASH, XMR): ").upper()

if name in ["ETC", "DASH", "XMR"]:
    print("The time period is from beginning of the month till today.\n"
          "And the same amount of days exactly one year ago.")

    past, present = get_data(name)

    past_price = to_period(past)
    present_price = to_period(present)

    one_simulation_past = moving_avg(past_price)
    one_simulation_present = moving_avg(present_price)

    avg_simulation_past = sim(past_price)
    avg_simulation_present = sim(present_price)

    plots(past_price, one_simulation_past, avg_simulation_past, "PAST")
    plots(present_price, one_simulation_present, avg_simulation_present, "PRESENT")
else:
    print("Wrong input")
