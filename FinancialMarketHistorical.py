# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 12:04:58 2020

@author: piotr
"""

import requests as rq
import json
import matplotlib.pyplot as plt
from datetime import datetime

def json_to_str(obj):
        text = json.dumps(obj,sort_keys=(True), indent = 4) 
        x = json.loads(text)
        return x


def hist_plot(response):
    
    date = []
    price = []
   
    x = json_to_str(response.json()) 
    
    idx = int(x[0]['tid'])
    
    # data plot
    for i in range(5):
        response = rq.get("https://bitbay.net/API/Public/BTCPLN/trades.json?since=" + str(idx))
        x = json_to_str(response.json()) 
        
        x = x[::-1]
        
        for j in x:
                date.append(j["date"])
                price.append(j["price"]) 
             
        idx -= 50 
    
    date = date[::-1]
    price = price [::-1]   
    
    
    #growth size and rate
    dif = [0]
    dift = [0]
    
    for i in range (len(price)-1):
        dif.append(price[i+1] - price[i])
        if (date[i+1] - date[i]) != 0:
            dift.append((price[i+1] - price[i])/(date[i+1] - date[i]))
        else: 
            dift.append(price[i+1] - price[i]) 
    
    
    local_ex_price = []
    local_ex_date = []
    
    #local extremum
    for i in range(len(date)-1):
        if (dift[i] >= 0) != (dift[i+1] >= 0):
            local_ex_price.append(price[i])
            local_ex_date.append(date[i])    
     
    #plot 
    #wykres szybkoć i wielkoci wzrostu jest na osobnym wykresie ponieważ skala wielkosci ceny do zmian jest tak duza ze wykres jest nieczytelny 
    plt.plot(date, price)
    plt.plot(local_ex_date, local_ex_price, 'ro')
    plt.show()    
     
    plt.plot(date, dif)
    plt.plot(date, dift)    
    plt.legend(['growth size','growth rate']) 
    
response = rq.get("https://bitbay.net/API/Public/BTCPLN/trades.json?sort=desc")        
hist_plot(response)