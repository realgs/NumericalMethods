import requests
import json
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd


def return_data_json(obj):
    
    text = json.dumps(obj,sort_keys=(True), indent = 4)
    
    return text


def get_data(url , headers):

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        text = return_data_json(response.json()) 
        text = json.loads(text)  
        prices = []
        dates = []
        for i in range(len(text)):
            prices.append(text[i]['price_close'])
            dates.append(text[i]['time_close'][:10])
        
    elif response.status_code == 429:
        print('Nieprawidłowy klucz api !!!')
        
    else:
        print('Wystąpił błąd' , response.status_code , '!')
       
    return prices , dates


def count_param(aver , std , n):
    
    normal = pd.DataFrame(np.random.normal(aver , std , n))
            
    param = abs(np.random.choice(normal[0]))
    
    return param


def predict_prices(prices):
    
    predicted_prices = []
    data_prices = prices.copy()
    
    for j in range(len(data_prices)):
        
        increases = []
        falls = []
        
        for i in range(len(data_prices)-1):
            change = (data_prices[i+1] - data_prices[i]) / data_prices[i]
            if change < 0:
                falls.append(change)
            elif change >= 0: 
                increases.append(change)
        
        prob = len(falls) / len(increases)
        
        param = count_param(1 , 1/3 , 100)
        
        if prob >= 1:
            predicted_price = data_prices[-1] * (1 + np.std(increases) * param)
        elif prob <1:
            predicted_price = data_prices[-1] * (1 - np.std(falls) * param)
            
        data_prices.append(predicted_price)
        predicted_prices.append(predicted_price)
        data_prices = data_prices[1:]
        
    return predicted_prices


def count_statistics(prices):
    
    average = np.mean(prices)
    standard_deviation = np.std(prices)
    median_stat = np.median(prices)
    
    return average , standard_deviation , median_stat


def print_statistics(average , standard_deviation , median_stat):
    
    print('\n...............Statystyki...............\nŚrednia:                ' 
          , round(average , 2) , '\nOdchylenie standardowe: ' 
          , round(standard_deviation , 2) , '\nMediana:                '
          , round(median_stat , 2))
    

def single_simulation(prices):
    
    predicted_prices  = predict_prices(prices)
    average , standard_deviation , median_stat = count_statistics(predicted_prices)
    print('\n\n..........POJEDYNCZA SYMULACJA..........')
    print_statistics(average , standard_deviation , median_stat)
    
    return predicted_prices


def multiple_simulation(n , prices):
    
    predictions = []
    
    for i in range(int(n)):
        predicted_prices  = predict_prices(prices)
        predictions.append(predicted_prices)
    
    statistics = []
    average_prices= []
    for i in range(len(predictions[0])):
        day_predictions = []
        for j in range(len(predictions)):
            day_predictions.append(predictions[j][i])
        average , standard_deviation , median_stat = count_statistics(day_predictions)
        statistics.append([average , standard_deviation , median_stat])
        average_prices.append(average)
    
    average , standard_deviation , median_stat = count_statistics(average_prices)
    print('\n\n..........WIELOKROTNA SYMULACJA..........')  
    print_statistics(average , standard_deviation , median_stat)
    
    return average_prices , predictions , statistics


def prediction_error(prices , predicted_prices , average_prices):
    
    prices = np.array(prices)
    predicted_prices = np.array(predicted_prices)
    average_prices = np.array(average_prices)
    
    single_error = np.sum((prices - predicted_prices)**2 / len(prices))
    multiple_error = np.sum((prices - average_prices)**2 / len(prices))
    
    return single_error , multiple_error


def print_plot(prices_0 , prices , predicted_prices , average_prices , dates_0 , dates , base_currency):
    
    plt.figure(figsize = (25 , 7))  
    plt.plot(dates_0, prices_0, '-o' , label = 'dataset prices')
    plt.plot(dates , predicted_prices, '-o' , label = 'predicted prices')
    plt.plot(dates , average_prices, '-o' , label = 'average predicted prices')
    plt.plot(dates , prices , '-o' , label = 'real prices')
    plt.xticks(dates_0 + dates, rotation='vertical')
    plt.xlabel('date')
    plt.ylabel('price ' + '[' + base_currency + ']')
    plt.title('SYMULACJA')
    plt.legend()
    plt.show()


def main():
    
    base_currency = input('Wprowadź walutę bazową (USD,EUR): ')  
    cryptocurrency  = input('Podaj kryptowalutę (BTC,LTC,ETH,XRP,BCH): ')  
    print('\nSymulacja była przeprowadzana np. dla zakresu 2018-11-01 ; 2019-01-01')    
    date_start_0 = input('Wpisz datę początkową (YYYY-MM-DD): ')
    date_end_0 = input('Wpisz datę końcową historycznych danych (YYY-MM-DD): ')
    
    url_0 = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_' +cryptocurrency + '_' + base_currency + '/history?period_id=1DAY&time_start=' +date_start_0 + 'T00:00:00&time_end=' + date_end_0 + '&limit=1000'
    headers = {'X-CoinAPI-Key' : '412B09B9-BDA1-484C-852E-80305673E2A6'}
    
    prices_0 , dates_0 = get_data(url_0 , headers)
    
    date_start = date_end_0
    (year, month, day) = dates_0[-1].split("-")
    data = datetime.date(int(year), int(month), int(day))
    date_end = str(data + datetime.timedelta(days = len(dates_0) + 1))
    
    url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_' +cryptocurrency + '_' + base_currency + '/history?period_id=1DAY&time_start=' +date_start + 'T00:00:00&time_end=' + date_end + '&limit=1000'
    
    n = input('Podaj ilosc symulacji w wielokrotnej symulacji: ')
    
    prices , dates = get_data(url , headers)
    predicted_prices = single_simulation(prices_0)
    average_prices , predictions , statistics = multiple_simulation(n , prices_0)
    single_error , multiple_error= prediction_error(prices , predicted_prices , average_prices)
    print('\n.............BŁĘDY SYMULACJI............\nPojedyncza symulacja    ' , round(single_error , 2) , '\nWielokrotna symulacja   ' , round(multiple_error , 2))
    print_plot(prices_0 , prices , predicted_prices , average_prices , dates_0 , dates , base_currency)
    
main()
