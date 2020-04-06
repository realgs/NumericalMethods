import requests
import time

def bitbay_order():

    response = requests.get("https://bitbay.net/API/Public/BTCEUR/orderbook.json")

    return response.json()

def bitbay_ticker():

    response = requests.get("https://bitbay.net/API/Public/BTCEUR/ticker.json")

    return response.json()

def order():

    BTC_to_EUR = bitbay_order()
    sale = BTC_to_EUR['asks']
    buy = BTC_to_EUR['bids']
    s=0
    b=0

    print("kupno")
    for i in range (5):
        print(buy[b])
        b=b+1

    print("")

    print("sprzedaz")
    for i in range (5):
        print(sale[s])
        s=s+1

def timeloop():
    while True:
        BTC_EUR = bitbay_ticker()

        sale = BTC_EUR['ask']
        buy = BTC_EUR['bid']
        diff = (((sale-buy)/buy)*100)
        print("")
        print("Bitcoin -> EUR")
        print("sprzedaz:",sale,"EUR")
        print("kupno:",buy,"EUR")
        print(diff,'%')

        time.sleep(5)

order()
timeloop()
