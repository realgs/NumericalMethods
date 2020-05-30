import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def create_list(date_start):
    response = requests.get('https://bitbay.net/API/Public/BTCUSD/trades.json?sort=desc').json()
    date_end=response[-1]['tid']
    done=False
    e=1
    while not done:
        p_response=requests.get('https://bitbay.net/API/Public/BTCUSD/trades.json?sort=desc&since='+str(int(date_end)-e*50)).json()
        for i in p_response:
            response.append(i)
        if response[-1]['date']<=date_start:
            done=True
        e+=1
    for i in range(len(response)):
        if response[i]['date']<date_start:
            response=response[:i]
            return response

def list_to_listbydays(list):
    days=[]
    for i in list:
        i['date']=datetime.fromtimestamp(i['date']).date()
        if {'date':i['date'],'price':0,'amount':0,'transactions':0} not in days:
            days.append({'date':i['date'],'price':0,'amount':0,'transactions':0})
    listbydays=[]
    for j in days:
        for i in list:
            if j['date']==i['date']:
                j['price']+=i['price']
                j['amount']+=i['amount']
                j['transactions']+=1

    for i in days:
        i['price']=i['price']/i['transactions']
    return list, days



def prediction(data, n=20):
    p=[]
    for i in data:
        p.append(i['price'])
    change=[]
    for i in range(len(p)-1):
        change.append(p[i+1]/p[i])
    import random
    predictions=[]
    predictions.append(p[-1]*random.choice(change))
    for i in range(n):
        predictions.append(predictions[i]*random.choice(change))
    return p, predictions


_,d=list_to_listbydays(create_list(1577836800))
predictions=[]

for i in range(100):
    _,pred=prediction(d,100)
    predictions.append(pred)

avg_pred=[]
for i in range(len(predictions[0])):
    x=0
    for j in range(100):
        x+=predictions[j][i]
    avg_pred.append(x/100)

x,y=prediction(d,100)
plt.plot(x+y,'r--')
plt.plot(x+avg_pred,)
plt.show()
