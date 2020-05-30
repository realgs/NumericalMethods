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

def shorten_list(list, date_end):
    for i in range(len(list)):
        if list[i]['date']<=date_end:
            return list[i:]

data = create_list(1588340800)
data_to = shorten_list(data, 1589500800)


predictions=[]
for i in range(100):
    x,pred = prediction(data_to,(len(data)-len(data_to)))
    predictions.append(pred)

avg_pred=[]
for i in range(len(predictions[0])):
    a=0
    for j in range(len(predictions)):
        a+=predictions[j][i]
    avg_pred.append(a/len(predictions))

true_data=[]
for i in data:
    true_data.append(i['price'])

plt.plot(x+pred,label='predicted values')
plt.plot(x+avg_pred,label='avergae predicted values')
plt.plot(true_data, label='true values')
plt.legend()
plt.show()
