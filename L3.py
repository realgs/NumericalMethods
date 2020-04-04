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

bitbay=bitbay_orders()
bb_ticker=bitbay_ticker()
bc_ticker=blockchain_ticker()





