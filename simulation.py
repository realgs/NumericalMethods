import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv
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
    else:
        print('Wystąpił błąd' , response.status_code , '!')
    
    return prices , dates


def count_param():
    
    normal = pd.DataFrame(np.random.normal(0 , 1 , 100))
            
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
        
        param = count_param()
        
        if prob >= 1:
            predicted_price = data_prices[-1] * (1 + np.std(increases) * param)
        elif prob <1:
            predicted_price = data_prices[-1] * (1 - np.std(falls) * param)
            
        data_prices.append(predicted_price)
        predicted_prices.append(predicted_price)
        data_prices = data_prices[1:]
        
    return predicted_prices


def create_dates(dates):
    
    last_date = dates[-1][:4] + '-' + dates[-1][5:10]
    new_dates= [last_date]
    
    for i in range(len(dates)):
        
        (year, month, day) = new_dates[-1].split("-")
        data = datetime.date(int(year), int(month), int(day))
        new_date = data+datetime.timedelta(days=1)
        
        new_dates.append(str(new_date))
        
    new_dates = new_dates[1:]
    
    return new_dates                  
    

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
    

def single_simulation(prices , dates , base_currency):
    
    
    predicted_prices  = predict_prices(prices)
    average , standard_deviation , median_stat = count_statistics(predicted_prices)
    print('\n\n..........POJEDYNCZA SYMULACJA..........')
    print_statistics(average , standard_deviation , median_stat)
    
    return predicted_prices
    
    
def multiple_simulation(n , prices , dates , base_currency):
    
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


def save_data(data , file):
    
    with open(file , 'w' , newline='') as csvfile:
        csvwriter = csv.writer(csvfile , delimiter=';')
        for row in data:
            csvwriter.writerow(row)
    csvfile.close()
    
    
def print_plot(prices , predicted_prices , average_prices , dates , new_dates , base_currency):
    
    plt.figure(figsize = (25 , 7))  
    plt.plot(dates, prices, '-o' , label = 'dataset prices')
    plt.plot(new_dates , predicted_prices, '-o' , label = 'predicted prices')
    plt.plot(new_dates , average_prices, '-o' , label = 'average predicted prices')
    plt.xticks(dates + new_dates, rotation='vertical')
    plt.xlabel('date')
    plt.ylabel('price ' + '[' + base_currency + ']')
    plt.title('SYMULACJA')
    plt.legend()
    plt.show()
  
    
def main():
    
    base_currency = input('Wprowadź walutę bazową (USD,EUR): ')  
    cryptocurrency  = input('Podaj kryptowalutę (BTC,LTC,ETH,XRP,BCH): ')        
    date_start = input('Podaj datę rozpoczęcia (format YYYY-MM-DD): ')
    
    url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_' +cryptocurrency + '_' + base_currency + '/history?period_id=1DAY&time_start=' +date_start + 'T00:00:00'
    headers = {'X-CoinAPI-Key' : '97B909F1-32DB-4ABA-BE04-DCF34E8EDDF5'}
    
    n = input('Podaj ilosc symulacji w wielokrotnej symulacji: ')
    
    prices , dates = get_data(url , headers)
    predicted_prices = single_simulation(prices , dates , base_currency)
    average_prices , predictions , statistics = multiple_simulation(n , prices , dates , base_currency)
    new_dates = create_dates(dates)
    print_plot(prices , predicted_prices , average_prices , dates , new_dates , base_currency)
    
    action = input('Czy chcesz zapisać wyniki iteracji wielokrotnej symulacji ?\n1. tak 2. nie\nAkcja:  ')
   
    if action == '1':
        save_data(predictions , 'prediction.csv')
        save_data(statistics , 'statistic.csv')
        print('Wyniki zostały zapisane.')
    else: 
        pass   
    
main()

