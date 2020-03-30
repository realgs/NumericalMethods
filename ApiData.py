import requests 
import json

def return_data_json(obj):
    
    text = json.dumps(obj,sort_keys=(True), indent = 4)
    return text

def sell_buy_offers(response):    
    
    json_data= return_data_json(response.json()) 
    to_dict = json.loads(json_data)
    
    bids=to_dict['bids']
    asks=to_dict['asks']
    
    display('BIDS','RATE,QUANTITY',bids,'ASKS','RATE,QUANTITY',asks)
    
def main():
    response = requests.get("https://bitbay.net/API/Public/BTC/orderbook.json")
    if response.status_code==200:
        sell_buy_offers(response)
    else:
        print('Wystąpił bład')
        
main()

