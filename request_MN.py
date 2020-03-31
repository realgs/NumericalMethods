import requests
import threading

def bitbay_data():

    response = requests.get("https://bitbay.net/API/Public/BTC/orderbook.json")

    return response.json()

def bitbay_data_ticker():

    response = requests.get('https://bitbay.net/API/Public/BTC/ticker.json')

    return response.json()

bitbay_BTC = bitbay_data_ticker()

orderbook_bitbay = bitbay_data()
ASKS_bitbay = orderbook_bitbay['asks']
BIDS_bitbay = orderbook_bitbay['bids']

print('first ten offers from bitbay\n')
print('SALE PRICE:')
for i in ASKS_bitbay[:10]:
    print(i,'\n')
print('BUY PRICE:')
for i in BIDS_bitbay[:10]:
    print(i,'\n')

def Five_second_rerun():

    bitbay_BTC = bitbay_data_ticker()

    sales_bitbay = bitbay_BTC['ask']
    buys_bitbay = bitbay_BTC['bid']

    calculate = ((buys_bitbay - sales_bitbay)/sales_bitbay) * 100

    print('Sale price:',sales_bitbay)
    print('Buy price:',buys_bitbay,'\n')
    print(calculate,'%')
    print('wait 5 seconds for next price and buy/sell ratio \n')
    threading.Timer(5, Five_second_rerun).start()

Five_second_rerun()
