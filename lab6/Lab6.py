{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "import json\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "ether = requests.get('https://bitbay.net/API/Public/ETH/trades.json')\n",
    "bitcoin = requests.get('https://bitbay.net/API/Public/BTC/trades.json')\n",
    "dash = requests.get('https://bitbay.net/API/Public/DASH/trades.json')\n",
    "litecoin = requests.get('https://bitbay.net/API/Public/LTC/trades.json')\n",
    "lisk = requests.get('https://bitbay.net/API/Public/LSK/trades.json')\n",
    "game = requests.get('https://bitbay.net/API/Public/GAME/trades.json')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [],
   "source": [
    "prices = {\n",
    "    'ETH': ether.json()[0]['price'],\n",
    "    'BTC': bitcoin.json()[0]['price'],\n",
    "    'DASH': dash.json()[0]['price'],\n",
    "    'LTC': litecoin.json()[0]['price'],\n",
    "    'LSK': lisk.json()[0]['price'],\n",
    "    'GAME': game.json()[0]['price']\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [],
   "source": [
    "wallet = {\n",
    "    'ETH': 10,\n",
    "    'BTC': 5,\n",
    "    'DASH': 3,\n",
    "    'LTC': 70,\n",
    "    'LSK': 25,\n",
    "    'GAME': 50,\n",
    "    'cash': 100000\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 67,
   "metadata": {},
   "outputs": [],
   "source": [
    "def transaction(crypto, quantity, type_t):\n",
    "    if type_t == 'sell' and wallet[crypto] >= quantity:\n",
    "        wallet[crypto] -= quantity\n",
    "        wallet['cash'] += quantity * prices[crypto]\n",
    "        status = 1\n",
    "    elif type_t == 'buy' and wallet['cash'] >= quantity * prices[crypto]:\n",
    "        wallet[crypto] += quantity\n",
    "        wallet['cash'] -= quantity * prices[crypto]\n",
    "        status = 1\n",
    "    else:\n",
    "        status = 0\n",
    "    print(wallet)\n",
    "    print('${:.2f}'.format(wallet['cash']))\n",
    "    return status\n",
    "   "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "crypto = input('ETH, BTC, DASH, LTC, LSK, GAME')\n",
    "quantity = int(input('quantity'))\n",
    "type_t = input('sell or buy ')\n",
    "transaction(crypto, quantity, type_t)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
