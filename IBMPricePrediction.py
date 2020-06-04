import requests as rq
import json
import matplotlib.pyplot as plt
import scipy.optimize as opt
import numpy as np
import datetime
import random

def API_call(obj):

    obj = rq.get(obj).json()
    text = json.dumps(obj,sort_keys=(True), indent = 4) 
    x = json.loads(text)
    return x

def regresion(x,y):
    def cost(ab):
        a,b = ab
        err = 0
        for i in range(len(x)):
            pre_y = a*x[i] + b
            err += (y[i] - pre_y)**2
        return err

    r_pocz=np.random.normal(0,10,size=2)
    r_opt=opt.fmin(cost,r_pocz)
    return r_opt

def random_date():
    latest  = datetime.date.today()
    earliest = datetime.date(year=latest.year-20, month=latest.month, day=latest.day-1)
    delta = latest - earliest
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds    
    random_second = random.randrange(int_delta)
    return earliest + datetime.timedelta(seconds = random_second)

def sim (a):
    #najpierw sprawdzam czy data nie jest w czasie weekendu kiedy nie ma notowań
    if a not in dates: 
        for i in range(2):
            dd = (int(a[8:10]))
            dd += 1
            a = a[:9] + str(dd)
            if a in dates:
                break
        if a not in dates:
            print("data poza zakresem lub w zlym formacie")
            return 

    N = dates.index(a)

    a,b = regresion(prices[N:len(dates)-5], prices[N+5:])   #wpływ cen z zeszłego tygodnia na ceny z tygodnia nastepnego (5 dni roboczch)

    predicted_prices = []
    
    for x in prices[len(dates)-522:len(dates)-261]: #261 to ok. liczba rekordów z poprzedniego roku, trochę się psuje przez weekendy
        predicted_prices.append(a*x+b) 
    return predicted_prices

API_KEY = 'ESJGNOSQE67NP8OM'
API2 = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=" + API_KEY

data = API_call(API2)['Time Series (Daily)']
dates = list(data.keys())

prices=[]
for i in range(len(dates)):
    prices.append(float(data[dates[i]]['4. close']))

keys = (data[dates[0]].keys())

a = '2012-12-12'#input("Podaj date w formacie rrrr-mm-dd (max 20 lat w stecz):")
predicted_prices = sim(a)




avg_pred = predicted_prices.copy()
for i in range(99):
    pred = None
    while pred == None:
        pred = sim(str(random_date()))
    for j in range(len(pred)):
        avg_pred[j] += pred[j]

for i in range(len(avg_pred)):
    avg_pred[i] = avg_pred[i]/100

plt.plot(prices[len(dates)-261:] + predicted_prices)
plt.plot(prices[len(dates)-261:] + avg_pred)
plt.plot(prices[len(dates)-261:])
plt.legend(['prediction','average prediction after 100 simulations', 'last yera'])
plt.show()   