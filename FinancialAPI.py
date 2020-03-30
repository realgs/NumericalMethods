import requests as rq
import json


def connect_API(url, params):
    waluta, kategoria = params
    url += '{}{}/{}.json'.format(waluta[0], waluta[1], kategoria)
    response = rq.get(url)
    return response


params = (['BTC', 'USD'], 'market')
url = "https://bitbay.net/API/Public/"
response = connect_API(url,params)
print(response.status_code)