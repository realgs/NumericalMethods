import requests
from matplotlib.pyplot import *
from numpy import *
import time

var, all_wolumens, rate = [], [], []


def request(market):
    url = f"https://api.bitbay.net/rest/trading/transactions/{market}?limit=300"
    response = requests.request("GET", url)
    before60 = float((time.time() + 3600))
    global rate
    rate = []
    for index in response.json()['items']:
        if float(index['t']) >= before60:
            rate.insert(0, float(index['r']))
    global var
    var = []
    for x in range(len(rate) - 1):
        var.append(rate[x] - rate[x - 1])
    global all_wolumens
    all_wolumens = []
    for i in response.json()['items']:
        if float(i['t']) >= before60:
            all_wolumens.insert(0, float(i['a']))
    plotsy(market)


def plotsy(market):
    subplot(2, 1, 1)
    title(f'wolumen in last hour in {market}')
    plot(all_wolumens, c='green')
    ylabel('wolumen')
    xlabel('quantity')

    subplot(2, 1, 2)
    title('difference of values')
    plot(var, c='red')
    ylabel('rate of diffrence')
    savefig('chart')
    show()


request('LSK-USD')
