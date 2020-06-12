import requests
import json
import matplotlib.pyplot as plt

r = requests.get('https://bitbay.net/API/Public/BTC/trades.json')
print(r.status_code)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


baza = r.json()
Sell = []
Buy = []

for i in baza:
    if i['type'] == 'sell':
        Sell.append(i)
    elif i['type'] == 'buy':
        Buy.append(i)

Buy_price = []
Buy_date = []

for i in Buy:
    Buy_date.append(i['date'])
    Buy_price.append(i['price'])

Sell_price = []
Sell_date = []

for i in Sell:
    Sell_date.append(i['date'])
    Sell_price.append(i['price'])

Buy_date = [i for i in range(len(Buy_date))]
Sell_date = [i for i in range(len(Sell_date))]

plt.figure(figsize=(10,5))
plt.plot(Buy_date, Buy_price, '-o', label = 'buy')
plt.plot(Sell_date, Sell_price, '-o', label = 'sell')
plt.xlabel('time', fontsize = 14)
plt.ylabel('price', fontsize = 14)
plt.legend()
plt.show()

from scipy.signal import argrelextrema
import numpy as np

Buy_price_a = np.array(Buy_price)
Sell_price_a = np.array(Sell_price)

a = Buy_price_a[argrelextrema(Buy_price_a, np.less)[0]]
b = Buy_price_a[argrelextrema(Buy_price_a, np.greater)[0]]
b_locals = np.concatenate((a, b), axis=None)

a = Sell_price_a[argrelextrema(Sell_price_a, np.less)[0]]
b = Sell_price_a[argrelextrema(Sell_price_a, np.greater)[0]]
s_locals = np.concatenate((a, b), axis=None)


ybl = []
ysl = []
x = argrelextrema(Buy_price_a, np.less) + argrelextrema(Buy_price_a, np.greater)
y = argrelextrema(Sell_price_a, np.less) + argrelextrema(Sell_price_a, np.greater)

for i in x:
    for j in range(len(i)):
        ybl.append(i[j])
for i in y:
    for j in range(len(i)):
        ysl.append(i[j])

plt.figure(figsize=(10,5))
plt.plot(Buy_date, Buy_price, '-o', label = 'buy')
plt.plot(Sell_date, Sell_price, '-o', label = 'sell')

plt.plot(ybl, b_locals, 'x', color = 'red', label = 'buy_locals')
plt.plot(ysl, s_locals, 'x', color = 'green', label = 'sell_locals')

plt.xlabel('time', fontsize = 14)
plt.ylabel('price', fontsize = 14)
plt.legend()
plt.show()