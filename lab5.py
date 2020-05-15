import requests
from matplotlib.pyplot import *
from numpy import *



def request():
    url = "https://api.bitbay.net/rest/trading/transactions/BTC-PLN?limit=300"
    response = requests.request("GET", url)
    return response.json()['items']

for i in request():
    print(i["t"])

now = float((time.time() - 3600) * 1000)

rate = []
for index in request():
    if float(index['t']) >= now:
        rate.insert(0, float(index['r']))

var = [0]
for x in range(len(rate) - 1):
    var.append(rate[x] - rate[x - 1])

all_wolumens = []
for i in request():
    if float(i['t']) >= now:
        all_wolumens.insert(0, float(i['a']))

subplot(2, 1, 1)
title('wolumens in last hour')
plot(all_wolumens, c='green')
ylabel('BTC')

subplot(2, 1, 2)
title('rate of changes')
plot(var, c='red')
ylabel('difference')

show()
