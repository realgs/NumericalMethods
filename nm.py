import requests
import numpy
from matplotlib.pyplot import*
import time as t

a = input("Jaka chcesz walute: \nBTC \nETH \nBCH \n")

def stats():

    if a == 'BTC':
        response = requests.get("https://www.bitstamp.net/api/v2/transactions/btcusd/")
    elif a == 'ETH':
        response = requests.get("https://www.bitstamp.net/api/v2/transactions/ethusd/")
    elif a == 'BCH':
        response = requests.get("https://www.bitstamp.net/api/v2/transactions/bchusd/")
    else:
        print('nie ma takiej waluty')
    return response.json()

def values():
    values=stats()
    change = []
    price=[]
    real_price=[]
    s_price=[]
   
    for i in range(len(values)):
        if values[i]["type"] == "0":
            price.append(float(values[i]["price"]))
          
    r=price[len(price)-1]
    
    for i in range(len(price)-2):
        change.append((price[i+1]/price[i]-1)*100)
    
    s=(sum(change)/len(change))*price[len(price)-2]+price[len(price)-2]
    
    return r, s

def predictions():
    r, s = values()
    
    for i in range(100):
        real_price.append(r)
        s_price.append(s)
        t.sleep(1)
    
    plot(real_price)
    plot(s_price)
    show()

predictions()