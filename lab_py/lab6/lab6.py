import requests
import json
import matplotlib.pyplot as plt

ether = requests.get('https://bitbay.net/API/Public/ETH/trades.json')
bitcoin = requests.get('https://bitbay.net/API/Public/BTC/trades.json')
dash = requests.get('https://bitbay.net/API/Public/DASH/trades.json')
litecoin = requests.get('https://bitbay.net/API/Public/LTC/trades.json')
lisk = requests.get('https://bitbay.net/API/Public/LSK/trades.json')
game = requests.get('https://bitbay.net/API/Public/GAME/trades.json')

prices = {
    'ETH': ether.json()[0]['price'],
    'BTC': bitcoin.json()[0]['price'],
    'DASH': dash.json()[0]['price'],
    'LTC': litecoin.json()[0]['price'],
    'LSK': lisk.json()[0]['price'],
    'GAME': game.json()[0]['price']
}

wallet = {
    'ETH': 10,
    'BTC': 5,
    'DASH': 3,
    'LTC': 70,
    'LSK': 25,
    'GAME': 50,
    'cash': 100000
}

def transaction(crypto, quantity, type_t):
    if type_t == 'sell' and wallet[crypto] >= quantity:
        wallet[crypto] -= quantity
        wallet['cash'] += quantity * prices[crypto]
        status = 1
    elif type_t == 'buy' and wallet['cash'] >= quantity * prices[crypto]:
        wallet[crypto] += quantity
        wallet['cash'] -= quantity * prices[crypto]
        status = 1
    else:
        status = 0
    print(wallet)
    print('${:.2f}'.format(wallet['cash']))
    return status

crypto = input('ETH, BTC, DASH, LTC, LSK, GAME')
quantity = int(input('quantity'))
type_t = input('sell or buy ')
transaction(crypto, quantity, type_t)

