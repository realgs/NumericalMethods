import requests

response = requests.get('https://bitbay.net/API/Public/BTCPLN/orderbook.json')

print('Bids: ')
for i in response.json()['bids']:
    print(i)

print('Asks: ')
for i in response.json()['asks']:
    print(i)





