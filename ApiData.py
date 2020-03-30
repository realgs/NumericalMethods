import requests 
import json
import time

def return_data_json(obj):
    
    text = json.dumps(obj,sort_keys=(True), indent = 4)
    return text

def sell_buy_offers(response):    
    
    json_data= return_data_json(response.json()) 
    to_dict = json.loads(json_data)
    
    bids=to_dict['bids']
    asks=to_dict['asks']
    
    display('BIDS','RATE,QUANTITY',bids,'ASKS','RATE,QUANTITY',asks)
    
def count_difference(response): 
    
    json_data = return_data_json(response.json()) 
    to_dict = json.loads(json_data) 
    
    actual_bid=to_dict['bids'][0][0]
    actual_ask=to_dict['asks'][0][0]
    
    return  round((1 - (actual_bid - actual_ask) / actual_ask),5)


def difference_every_5s(response):    

    t0 = time.time()
    
    while True:
        t = time.time()
        if t-t0 >= 5:
            t0 = t
            response = requests.get("https://bitbay.net/API/Public/BTC/orderbook.json")
            print('SELL-BUY DIFFFERENCE:',count_difference(response))
        
def main():
    response = requests.get("https://bitbay.net/API/Public/BTC/orderbook.json")
    if response.status_code==200:
        sell_buy_offers(response)
        difference_every_5s(response)
    else:
        print('Wystąpił bład')
        
main()
