import requests
from time import sleep

while True:
    response = requests.get('https://bitbay.net/API/Public/BTCPLN/orderbook.json')
    print('Bids: ')
    for i in response.json()['bids']:
        print(i)
    print('\n')
    print('Asks: ')
    for i in response.json()['asks']:
        print(i)
    response = requests.get('https://bitbay.net/API/Public/BTCUSD/ticker.json')
    bid = response.json()['bid']
    ask = response.json()['ask']
    var = 1 - (bid - ask) / ask
    print('\nPercentage ratio of (bid-ask/ask) = ', var)
    sleep(5)
