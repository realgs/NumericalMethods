import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

bitcoin = requests.get('https://bitbay.net/API/Public/BTC/trades.json')

t = [i['date'] for i in bitcoin.json()]
btc = [i['price'] for i in bitcoin.json()]
time = []
for i in t:
    ts = datetime.utcfromtimestamp(i).strftime(' %H:%M')
    time.append(ts)
time_brown = time.copy()
time_brown.append('12:15')

#Model Browna
brown = np.zeros(len(btc)+1)
brown[0] = btc[0]
brown[1] = btc [1]
alfa = 0.8
for i in range(2,len(time_brown)):
    brown[i] = alfa*btc[i-1] + (1-alfa)*brown[i-1]

plt.figure(figsize = (15,5))
plt.plot(time, btc, '-o', label = 'BTC')
plt.plot(time_brown, brown, '-o', label = 'brown prediction')
plt.xticks(time_brown, rotation='vertical')
plt.legend()
plt.show()
