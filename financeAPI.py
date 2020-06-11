import requests
import time


def bitbay():
    while True:
        response = requests.get("https://bitbay.net/API/Public/BTC/ticker.json")
        data = response.json()
        percentage = ((data['ask'] - data['bid']) / data['bid']) * 100
        print("Record of Bitcoin exchange rate on Bitbay: \n{} \nand percentage of aks/bids diffrence: {}".format(data, percentage))
        print(40 * "=")
        time.sleep(5)


bitbay()