import requests as r
import time as t
a=0
def data():
    response = r.get('https://bitbay.net/API/Public/BTCPLN/ticker.json')
    return response.json()

def order():
    response = r.get('https://bitbay.net/API/Public/BTCPLN/orderbook.json')
    return response.json()

orderbook=order()

for i in range(5):
    print(orderbook['bids'][i],'\n')
    print(orderbook['asks'][i],'\n')

def info():
    while True:
        BTC = data()
        sales = BTC['ask']
        buys = BTC['bid']
        calculate = 1-((sales-buys)/buys)
        print('Sale price:',sales,'pln')
        print('Buy price:',buys,'pln')
        print(calculate,'%','\n')
        t.sleep(5)
    
info(