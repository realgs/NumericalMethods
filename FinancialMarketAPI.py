# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:08:57 2020

@author: piotr
"""

import requests as rq
import json
import time


response = rq.get("https://bitbay.net/API/Public/BTC/orderbook.json")

def json_to_str(obj):
        text = json.dumps(obj,sort_keys=(True), indent = 4)
        return text
    


def print_offers(response):    
    x = json_to_str(response.json()) 
    
    y = json.loads(x)
    
    print("Buy offers [rate, quantity]") 
    for i in y['bids']:
        print(i)
    
    print("Sell offers [rate, quantity]") 
    for i in y['asks']:
        print(i)
        
print_offers(response)
    
def offers_diff(response):    
    x = json_to_str(response.json()) 
    
    y = json.loads(x) 
    return  1 - (y['bids'][0][0] - y['asks'][0][0]) / y['asks'][0][0]


def print_diff_every_5():    
    response = rq.get("https://bitbay.net/API/Public/BTC/orderbook.json")
    offers_diff(response)
    
    t1 = time.time()
    t2 = time.time()
    
    
    while (1<2):
        t2 = time.time()
        if t2-t1 >= 5:
            t1 = t2
            response = rq.get("https://bitbay.net/API/Public/BTC/orderbook.json")
            print(offers_diff(response)) 

print_diff_every_5()





