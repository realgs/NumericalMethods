import requests as rq
import pandas as pd


def download_markets():
    url = 'https://rest.coinapi.io/v1/symbols?apikey=28C36F0A-D3CE-400E-B168-9053C8E1F8AE'
    response = pd.DataFrame(rq.get(url).json())
    response.to_json(r'markets.json', orient='records')
    return response

