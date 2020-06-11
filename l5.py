import requests
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import pearsonr

def get_transactions(n=1):
    last_transaction=(requests.get('https://bitbay.net/API/Public/BTCUSD/trades.json?sort=desc')).json()[0]['tid']
    prices=[]
    for i in range(n):
        response = requests.get('https://bitbay.net/API/Public/BTCUSD/trades.json?sort=desc&since='+str(int(last_transaction)-i*50))
        for i in response.json():
            prices.append(i)
    return prices
tran=get_transactions(100)
for i in tran:
    i['date']=datetime.fromtimestamp(i['date']).date()

dates=[]
transactions_by_day=[]
day=[]
for i in tran:
    if len(dates)==0 or i['date']!= dates[-1]:
        if len(day)>0:
            transactions_by_day.append(day)
        dates.append(i['date'])
        day=[]
    day.append(i)
transactions_by_day.append(day)

w=[]
p=[]

for i in range(len(dates)):
    wd=0
    pd=0
    for j in transactions_by_day[i]:
        wd+=j['amount']
        pd+=j['price']
    w.append(wd)
    p.append(pd/len(transactions_by_day[i]))
for i in range(len(p)-1):
    p[i]=p[i+1]-p[i]
p.pop()
dates.pop()
w.pop()

c, _ = pearsonr(p,w)
plt.plot(dates,w,label="amount")
plt.plot(dates,p,label="price")
plt.legend()
plt.title("Correlation: "+str(c))
plt.savefig('correlation.png')
plt.show()
