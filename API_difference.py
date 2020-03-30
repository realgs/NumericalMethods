import requests
import time
while True:
    response = requests.get('https://bitbay.net/API/Public/BTCUSD/ticker.json')
    bid = response.json()['bid']
    ask = response.json()['ask']
    print(1-(bid-ask)/ask)
    time.sleep(5)
