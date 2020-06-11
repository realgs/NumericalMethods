import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import math

def return_data_json(obj):
    
    text = json.dumps(obj,sort_keys=(True), indent = 4)
    
    return text

def get_data(currency , date_start):
    
    url_1 = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_'+currency+'_USD/history?period_id=1MTH&time_start='+date_start+'T00:00:00'
    headers = {'X-CoinAPI-Key' : '.......API...KEY...........'}
    response = requests.get(url_1 , headers=headers)
   
    text = return_data_json(response.json())
    text = json.loads(text)

    dates = []
    prices = []
            
    for i in range(len(text)):
        dates.append(text[i]['time_close'][:7])
        prices.append(text[i]['price_close'])
            
    for i in range(len(dates)):
        dates[i] = dates[i][5:7] + '\n' + dates[i][:4]
   
    return dates , prices

def time_window_signal(prices):
    
    sigma = 0.3
    N = len(prices)
    
    w = np.zeros(N)
    for i in range(N):
        w[i] = math.exp(-1/2 * ((i - (N-1)/2) / (sigma * (N-1)/2)) **2)
    
    g = prices * w
    
    return g

def hossa_point(g , dates):
    
    hossa = max(g)
    index_hossa = list(g).index(hossa)
    date_hossa = dates[index_hossa]
    
    return date_hossa , hossa

def count_indicators(g , hossa):
    
    indicator_hossa = hossa / g[0]
    indicator_bessa = g[-1] / hossa

    return indicator_hossa , indicator_bessa

def print_plot(dates , g , date_hossa , hossa , currency):
    
    plt.figure(figsize = (25 , 5))        
    plt.plot(dates , g , '-o' , label = 'cena')
    plt.plot(date_hossa , hossa, 'o' , color = 'red' , label = 'koniec hossy\npoczątek bessy')
    plt.plot(dates[0] , g[0] , 'o' , color = 'black', label = 'początek hossy')
    plt.plot(dates[-1] , g[-1] , 'o' , color = 'purple' , label = 'koniec bessy')
    plt.title(currency)
    plt.xlabel('data')
    plt.ylabel('sygnał g')
    plt.legend()
    

def main():

    currencies=['BTC','LTC','ETH','XRP','BCH']
    
    currencies_indicators={}
    hossa_indicators=[]
    bessa_indicators=[]
    
    date_start = input('Wprowadź datę początkową (format YYYY-MM-DD): ')
    
    for currency in currencies:
        dates , prices = get_data(currency , date_start)
        g = time_window_signal(prices)
        date_hossa , hossa = hossa_point(g , dates)
        indicator_hossa , indicator_bessa = count_indicators(g , hossa)
        print_plot(dates , g , date_hossa , hossa , currency)
        currencies_indicators[currency] = indicator_hossa , indicator_bessa
        hossa_indicators.append(indicator_hossa)
        bessa_indicators.append(indicator_bessa)
    
    hossa_indicators.sort(reverse=True)
    bessa_indicators.sort(reverse=True)
    
    print(hossa_indicators,bessa_indicators)
    
    for key , value in currencies_indicators.items():
        if value[0] == hossa_indicators[0]:
            best_hossa = key
        if value[1] == bessa_indicators[0]:
            best_bessa = key
    
    print('Najlepszy w hossie: ', best_hossa , '\nNajlepszy w bessie: ' , best_bessa)
    
main()

