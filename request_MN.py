import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.signal import argrelextrema

def bitbay_data_history():

    response = requests.get("https://bitbay.net/API/Public/BTC/trades.json")

    return response.json()


bitbay_BTC_history = bitbay_data_history()

print(bitbay_BTC_history)

price_history = []
amount_history = []
date_history = []

for i in range(len(bitbay_BTC_history)):
    price_history.append(bitbay_BTC_history[i]['price'])
    amount_history.append(bitbay_BTC_history[i]['amount'])
    date_history.append(bitbay_BTC_history[i]['date'])

date = []
for i in range(len(date_history)):

    sub = datetime.datetime.fromtimestamp(date_history[i]).strftime('%Y: %H:%M:%S')
    date.append(sub)

def plot_with_extremum(data,label_x,label_y,name):

    x = data
    x_as_array = np.asarray(x)
    maximums_indexes = argrelextrema(nip, np.greater)
    maxima = []

    for i in range(len(maximums_indexes)):
        sub = maximums_indexes[i]
        maxima.append(x_as_array[sub])

    minimums_indexes = argrelextrema(nip, np.less)
    minima = []

    for i in range(len(minimums_indexes)):
        sub = minimums_indexes[i]
        minima.append(x_as_array[sub])

    plt.plot(x)
    plt.plot(minimums_indexes,minima, 'o')
    plt.plot(maximums_indexes,maxima,'o')
    plt.ylabel(label_y)
    plt.xlabel(label_x)
    plt.title(name)
    plt.show()

def plot_numbers_with_date(data,date, label_x,label_y, name):

    x = data
    y = date
    plt.plot_date(y,x,'-o', ydate = False)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(name)
    plt.show()

plot_numbers_with_date(price_history,date,'date','prices','price history with dates')
plot_with_extremum(price_history,'i','prices','price history Extremum')


