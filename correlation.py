import requests
import json
import numpy as np
import math 
import matplotlib.pyplot as plt


def return_data_json(obj):
    
    text = json.dumps(obj,sort_keys=(True), indent = 4)
    
    return text


def get_data(response):
    
    
    text = return_data_json(response.json())
    text = json.loads(text)

    return text 


def get_value_volume(text):

    volumes = np.zeros(len(text))
    values = np.zeros(len(text))
    
    for i in range(len(text)):
        volumes[i] = text[i]['volume_traded']
        values[i] = text[i]['price_close']
        
    return values , volumes


def count_indicators(values):
    
    indicators= np.zeros(len(values))
    
    for i in range(1,len(values)):
        indicators[i] = (values[i] - values[i-1]) / values[i-1]
    
    return indicators


def count_pearson(volumes , indicators):

    counter = len(volumes) * np.sum(volumes * indicators) - np.sum(volumes) * np.sum(indicators)
    denominator = math.sqrt((len(volumes) * np.sum(volumes*volumes) - (np.sum(volumes))**2) * (len(indicators) * np.sum(indicators * indicators) - (np.sum(indicators))**2))
    
    r=counter/denominator
    
    return r


def correlation(r):
    
    if r == 0:   
        correlation = 'brak korelacji'
        
    elif r < 0 and r >= -1:    
        if r >= -0.3:
            correlation = 'Słaba, ujemna korelacja'
        elif r >= -0.5:
            correlation = 'Umiarkowana, ujemna korelacja'
        elif r >= -0.7:
            correlation = 'Silna, ujemna korelacja'
        elif r >= -1:
            correlation = 'Bardzo silna, ujemna korelacja'
            
    elif r > 0 and r <= 1:
        if r <= 0.3:
            correlation = 'Słaba, dodatnia korelacja'
        elif r <= 0.5:
            correlation = 'Umiarkowana, dodatnia korelacja'
        elif r <= 0.7:
            correlation = 'Silna, dodatnia korelacja'
        elif r <= 1:
            correlation = 'Bardzo silna, dodatnia korelacja'
            
    elif r > 1 or r < -1:
        correlation = 'wartosc wychodzi poza zakres'
    
    return correlation


def plot(volumes , indicators , str_correlation , r):

    plt.plot(volumes , indicators, 'o')
    plt.title(str_correlation + '\nWspółczynnik Pearsona: ' + str(round(r,2)))
    plt.xlabel('Wolumen')
    plt.ylabel('Wskaźnik waloru')
    plt.savefig('correlation.png')
    
    
def main():
    
    date_start = input('Wprowadź datę początkową (format YYYY-MM-DD): ')
    currency = input('Wprowadź nazwę kryptowaluty (np.BTC,LTC,ETH,XRP,BCH): ')
    period = input('Wprowadź zakres (np.1SEC,1MIN,1HRS,1DAY,1MTH,1YRS): ')
    
    url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_' + currency + '_USD/history?period_id=' + period + '&time_start=' + date_start + 'T00:00:00'                           
    headers = {'X-CoinAPI-Key' : '.......API..KEY.........'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        
        text = get_data(response)
        values , volumes = get_value_volume(text)
        indicators = count_indicators(values)
        r = count_pearson(volumes , indicators)
        str_correlation = correlation(r)
        plot(volumes , indicators , str_correlation , r)
        
    else:
        print('Wystąpił błąd ' , response.status_code , '!')
    
main()