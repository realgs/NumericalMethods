#!/usr/bin/env python
# coding: utf-8

import requests as rq

def bitbay_orders():
    r=rq.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json")
    return r.json()

def bitbay_ticker():
    r=rq.get("https://bitbay.net/API/Public/BTCPLN/ticker.json")
    return r.json()

def blockchain_ticker():
    r=rq.get("https://blockchain.info/ticker")
    return r.json()

def orderbook():
    orders=bitbay_ordsers()
    sale=orders["asks"]
    buy=orders["bids"]
    
    n=0
    m=0
    
    print("Sale:")
    for i in range (10):
        print(sale[n])
        n+=1
    
    print("Buy:")
    for i in range (10):
        print(buy[m])
        m+=1
orderbook()