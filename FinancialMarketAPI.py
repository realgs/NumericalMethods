# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:08:57 2020

@author: piotr
"""

import requests as rq
import json



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
    





