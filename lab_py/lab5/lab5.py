import requests
import json
import matplotlib.pyplot as plt

r = requests.get('https://bitbay.net/API/Public/BTCUSD/trades.json')
print(r.status_code)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

from datetime import datetime
import numpy as np

baza = r.json()
Sell = []
Buy = []

for i in baza:
    if i['type'] == 'sell':
        ts = int(i['date'])
        i['date'] = datetime.utcfromtimestamp(ts).strftime('%H')
        Sell.append(i)
    elif i['type'] == 'buy':
        ts = int(i['date'])
        i['date'] = datetime.utcfromtimestamp(ts).strftime('%H')
        Buy.append(i)

date = ['08', '09', '10', '11', '12']
Sell_amount = np.zeros(len(date))
Sell_price = np.zeros(len(date))
Buy_amount = np.zeros(len(date))
Buy_price = np.zeros(len(date))
Sell_p = np.zeros(len(date))
Buy_p = np.zeros(len(date))
index = np.zeros(len(date))
values = np.zeros(len(date))

for i in range(len(date)):
    for j in Sell:
        if j['date'] == date[i]:
            Sell_amount[i] += float(j['amount'])
            Sell_p[i] += float(j['price'])

for i in range(len(date)):
    for j in Buy:
        if j['date'] == date[i]:
            Buy_amount[i] += float(j['amount'])
            Buy_p[i] += float(j['price'])

for i in range(len(date)):
    if Sell_amount[i] != 0 and Buy_amount[i] != 0:
        index[i] = Sell_amount[i] / Buy_amount[i]
        values[i] = Sell_p[i] / Buy_p[i]

plt.plot(date, index, '-o', label='volume(b/s)')
plt.plot(date, values, '-o', label='values(price b/s)')
plt.xlabel('hour', fontsize=12)
plt.legend()
plt.show()

ether = requests.get('https://bitbay.net/API/Public/ETH/trades.json')
bitcoin = requests.get('https://bitbay.net/API/Public/BTC/trades.json')
dash = requests.get('https://bitbay.net/API/Public/DASH/trades.json')
litecoin = requests.get('https://bitbay.net/API/Public/LTC/trades.json')
lisk = requests.get('https://bitbay.net/API/Public/LSK/trades.json')
game = requests.get('https://bitbay.net/API/Public/GAME/trades.json')
print(ether.status_code)

baza = ether.json()
time = [i for i in range(len(baza))]
eth = [i['price'] for i in ether.json()]
btc = [i['price'] for i in bitcoin.json()]
ds = [i['price'] for i in dash.json()]
ltc = [i['price'] for i in litecoin.json()]
lsk = [i['price'] for i in lisk.json()]
gm = [i['price'] for i in game.json()]

plt.figure(figsize = (15,5))
plt.plot(time, eth, '-o', label = 'ETH')
plt.plot(time, btc, '-o', label = 'BTC')
plt.plot(time, ds, '-o', label = 'DASH')
plt.plot(time, ltc, '-o', label = 'LTC')
plt.plot(time, lsk, '-o', label = 'LSK')
plt.plot(time, gm, '-o', label = 'GAME')
plt.legend()
plt.show()
