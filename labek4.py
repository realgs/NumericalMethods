import requests
from matplotlib.pyplot import *
import datetime
from numpy import *

url = "https://api.bitbay.net/rest/trading/transactions/BTC-pln"
headers = {'content-type': 'application/json','fromtime':'1487891243900'}
params={'limit':'300'}
response = requests.request("GET", url, headers=headers, params=params)

buys=[]
buys_times=[]
sells=[]
sells_times=[]
data_buy=[]
data_sell=[]

for order in response.json()['items']:
    if order['ty'] == 'Buy':
        buys.insert(0,float(order['r']))
        buys_times.insert(0, order['t'])
print('\n')
for order in response.json()['items']:
    if order['ty'] == 'Sell':
        sells.insert(0,float(order['r']))
        sells_times.insert(0, order['t'])

for i in range(len(buys_times)):
    db=datetime.datetime.fromtimestamp(int(buys_times[i])/1000).strftime('%Y-%m-%d %H:%M:%S')
    data_buy.append(db)

for i in range(len(sells_times)):
    ds=datetime.datetime.fromtimestamp(int(sells_times[i])/1000).strftime('%Y-%m-%d %H:%M:%S')
    data_sell.append(ds)

subplot(1,2,1)
plot(data_buy,buys, label='Price')
title('Buy PLN-BTC')
xlabel('Date [UTC+1]')
ylabel('Price [PLN]')
x_ticks = arange(0,len(data_buy)-40, 20)
xticks(x_ticks)
legend()

subplot(1,2,2)
plot(data_sell,sells, label='Price')
title('sell PLN-BTC')
xlabel('Date [UTC+1]')
ylabel('Price [PLN]')
x_ticks = arange(0,len(data_sell)-20, 15)
xticks(x_ticks)
legend()
fig = gcf()
fig.set_size_inches(36, 14)

show()