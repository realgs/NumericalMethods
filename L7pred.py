import requests
import numpy
from matplotlib.pyplot import *
import time

def choose_data():
    
    
    a=input("Wybierz nr waluty: \n BTC-1 \n ETH-2 \n BCH-3 \n")
    
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

    for i in range(len(values)):
        if values[i]["type"] == "0":
            price.append(float(values[i]["price"]))
    
    for i in range(len(price)-1):
        
        if price[i]<price[i+1]:
            updown.append(1)
            
        elif price[i]>price[i+1]:
            updown.append(0)
            
    for i in range(len(price)-1):
        b=((price[i+1]/price[i])-1)*100
        change.append(b)
    
    c=(sum(updown)/len(updown))
    
    
    if c > 0.5:
        print("Istnieje większe prawdopodobieństwo na wzrost wartości waluty w najbliższym czasie")
    elif c == 0.5:
        print("Najprawdopodobniej waluta utrzyma wartość")
    elif c < 0.5:
        print("Istnieje większe prawdopodobieństwo na spadek wartośći waluty w najbliższym czasie")
        
    title("Kurs historyczny")
    plot(change)
    show()
    
    print("TRWA SZACOWANIE PRZYSZŁEGO KURSU, CZEKAJ \n")
    for i in range(100):
        for i in range(len(values)):
            if values[i]["type"] == "0":
                predprice.append(float(values[i]["price"]))
                
        for i in range(len(predprice)-1):
            e=((predprice[i+1]/predprice[i])-1)*100
            predchange.append(e)
        
        y=sum(predchange)/len(predchange)
        pred.append(y)
        for i in range(len(predchange)):
            numpy.delete(predchange, i)
        time.sleep(5)
        
    title("Przewidywany kurs")
    plot(pred)
    show()

        
    
    

values = choose_data()
price = []
predprice = []
updown = []
change = []
predchange = []
pred = []
trades()

