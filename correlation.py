import requests
import json
import numpy as np
import math 
import matplotlib.pyplot as plt


def return_data_json(obj):
    
    text = json.dumps(obj,sort_keys=(True), indent = 4)
    
    return text


def get_data():

    date_start = input('Wprowadź datę początkową (format YYYY-MM-DD): ')
    currencies = input('Wprowadź nazwy kryptowalut (np.BTC,LTC,ETH,XRP,BCH): ')
    currencies = currencies.split(" ")
    period=input('Wprowadź zakres (np.1SEC,1MIN,1HRS,1DAY,1MTH,1YRS): ')
    
    url_1 = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_' + currencies[0] + '_USD/history?period_id=' + period + '&time_start=' + date_start + 'T00:00:00'
    url_2 = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_' + currencies[1] + '_USD/history?period_id=' + period + '&time_start=' + date_start + 'T00:00:00'
    headers = {'X-CoinAPI-Key' : '412B09B9-BDA1-484C-852E-80305673E2A6'}
    response_1 = requests.get(url_1, headers=headers)
    response_2 = requests.get(url_2, headers=headers)
    
    text_1 = return_data_json(response_1.json())
    text_1 = json.loads(text_1)
    text_2 = return_data_json(response_2.json())
    text_2 = json.loads(text_2)

    return text_1,text_2,currencies


def count_indicators(text_1,text_2):

    volumes_traded_1 = np.zeros(len(text_1))
    prices_1 = np.zeros(len(text_1))
    
    for i in range(len(text_1)):
        volumes_traded_1[i] = text_1[i]['volume_traded']
        prices_1[i] = text_1[i]['price_close']
        
    volumes_traded_2 = np.zeros(len(text_2))
    prices_2 = np.zeros(len(text_2))
    
    for i in range(len(text_2)):
        volumes_traded_2[i] = text_2[i]['volume_traded']
        prices_2[i] = text_2[i]['price_close']
        
    indicators_1 = np.array(prices_1)/np.array(volumes_traded_1)
    indicators_2 = np.array(prices_2)/np.array(volumes_traded_2)
    
    return indicators_1,indicators_2


def count_pearson(indicators_1,indicators_2):

    counter = len(indicators_1) * np.sum(indicators_1 * indicators_2) - np.sum(indicators_1) * np.sum(indicators_2)
    denominator = math.sqrt((len(indicators_1) * np.sum(indicators_1*indicators_1) - (np.sum(indicators_1))**2) * (len(indicators_2) * np.sum(indicators_2 * indicators_2) - (np.sum(indicators_2))**2))
    
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


def plot(indicators_1,indicators_2,str_correlation,currencies,r):

    plt.plot(indicators_1, indicators_2, 'o')
    plt.title(str_correlation + '\nWspółczynnik Pearsona: ' + str(round(r,2)))
    plt.xlabel('wskaźnik ' + currencies[0])
    plt.ylabel('wskaźnik ' + currencies[1])
    plt.savefig('correlation.png')
    
    
def main():
    text=get_data()
    indicators=count_indicators(text[0],text[1])
    r=count_pearson(indicators[0],indicators[1])
    str_correlation=correlation(r)
    plot(indicators[0],indicators[1],str_correlation,text[2],r)
    
main()