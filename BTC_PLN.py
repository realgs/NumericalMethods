import requests
import time


def bitbay_orderbook():

    response = requests.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json")

    return response.json()

def orderbook():
    
    order_BTC_PLN = bitbay_orderbook()
    sale = order_BTC_PLN['asks']
    buy = order_BTC_PLN['bids']
    a=0
    b=0
    
    print("SALE")
    for i in range (10):
        print(sale[a])
        a=a+1
    
    print("BUY")
    for i in range (10):
        print(buy[b])
        b=b+1
    

def bitbay_ticker():

    response = requests.get("https://bitbay.net/API/Public/BTCPLN/ticker.json")

    return response.json()


def timeloop():
    
    while True:
        BTC_PLN = bitbay_ticker()
        
        sale = BTC_PLN['ask']
        buy = BTC_PLN['bid']
        diff = (1-((sale-buy)/buy))
        print(" ")
        print("Bitcoin -> PLN")
        print("Sale:",sale,"PLN")
        print("Buy:",buy,"PLN")
        print(diff,'%')

        time.sleep(5)

orderbook()
timeloop()
