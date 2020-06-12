import requests
import json
import time


r = requests.get('https://bitbay.net/API/Public/BTC/trades.json')
print(r.status_code)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(r.json())

status = 0
s = r.json()[0]['price']
b = r.json()[4]['price']
while (status == 0):
    r = requests.get('https://bitbay.net/API/Public/BTC/trades.json')
    data = r.json()
    for i in data:
        if i['type'] == 'sell':
            s = i['price']
        elif i['type'] == 'buy':
            b = i['price']

        print(round(1 - ((s - b) / b), 5))
        time.sleep(5)

