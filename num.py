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
    price=[]
    for i in range(len(values)):
        if values[i]["type"] == "0":
            price.append(float(values[i]["price"]))
    
    return price
        
def predictions():
    price=values()
    up_down = []
    change = []
    change_all = []
    for i in range(len(price)-1):

            if price[i]<price[i+1]:
                up_down.append(1)
            elif price[i]>price[i+1]:
                up_down.append(0)

            change.append((price[i+1]/price[i]-1)*100)
    
    x = sum(up_down)/len(up_down)
    
    if x<0.5:
        print('Cena najprawdopodobniej spadnie.')
    elif x==0.5:
        print('Cena najprawdopodobniej się nie zmieni')
    else:
        print('Cena najprawdopodobniej wzrośnie.')
    
    for i in range(100):
        price1=values()
        change1 = []
        for i in range(len(price1)-1):
            change1.append((price1[i+1]/price1[i]-1)*100)

        y = sum(change1)/len(change1)
        change_all.append(y)
        t.sleep(5)
        
    plot(change_all)
    show()
    plot(change)
    show()
    
predictions()