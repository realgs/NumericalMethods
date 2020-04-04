import requests
import time


def get_offers(url, currencies, to_console):
    url += currencies[0]+currencies[1]+'/orderbook.json'
    response = requests.get(url).json()

    if to_console == True:
        print("\nOferty kupna oraz Ilości: \n", response['bids'])
        print("Oferty szprzedaży oraz Ilości: \n", response['asks'])

    return response

#Available currencies: ['PLN', 'EUR', 'USD', 'USDC', 'GBP']


def main():
    currencies = ['BTC', 'PLN']
    url = "https://bitbay.net/API/Public/"
    get_offers(url, currencies, True)

    i = int(input('\nIle razy odświeżyć? (-1 = inf):  '))

    while i > 0 or i == -1:
        if i > 0:
            i -= 1
        response = get_offers(url, currencies, False)
        buying = response['bids'][0][0]
        selling = response['asks'][0][0]
        difference = selling*100/buying - 100
        print('\nW ostatniej parze, oferta sprzedaży jest o', str(difference)+'% droższa od kupna')
        time.sleep(5)

main()