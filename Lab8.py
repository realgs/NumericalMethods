import requests
import numpy
from matplotlib.pyplot import *
import time

def choose_data():

    if a=="1":
        response = requests.get("https://www.bitstamp.net/api/v2/transactions/btcusd")

    elif a=="2":
        response = requests.get("https://www.bitstamp.net/api/v2/transactions/ethusd")

    elif a=="3":
        response = requests.get("https://www.bitstamp.net/api/v2/transactions/bchusd")

    else:
        print("Niepoprawne dane \n")

    return response.json()


def trades():
    
    change = []
    price = []

    for i in range(len(values)):
        if values[i]["type"] == "0":
            price.append(float(values[i]["price"]))
            

    real=price[len(price)-1]
    

    for i in range(len(price)-1):
        b=((price[i+1]/price[i])-1)*100
        change.append(b)
    
    sr=sum(change)/len(change)
    new=(1+sr)*price[len(price)-2]
    
    
    
    return real, new
    


realprice = []
simprice = []

a=input("Wybierz nr waluty: \n BTC-1 \n ETH-2 \n BCH-3 \n")

for i in range(100):

    values = choose_data()
    real, new = trades()

    realprice.append(real)
    simprice.append(new)
    time.sleep(2)

plot(realprice, label="rzeczywisty")
plot(simprice, label="symulacja")
legend(loc="upper right")
show()




