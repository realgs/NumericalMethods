import csv
import requests
import json
import numpy as np


def get_wallet(file):
    
    with open(file , newline='') as csvfile:       
        data = csv.reader(csvfile, delimiter=';')
        data_list = list(data)
        data_list = data_list[1:]
        currencies = []
        amount = []
        buy_prices_USD = []
        buy_prices_EUR = []
        
        for row in data_list:         
            currencies.append(row[0])
            amount.append(float(row[1]))
            buy_prices_USD.append(float(row[2]))
            buy_prices_EUR.append(float(row[3]))
            
    csvfile.close()
            
    return data_list , currencies , amount , buy_prices_USD , buy_prices_EUR



def return_data_json(obj):
    
    text = json.dumps(obj,sort_keys=(True), indent = 4)
    
    return text



def get_data(currencies ,  base_currency , amount):
    
    data_dict={}
    not_in_base=[]
    
    for currency in currencies:
        
        url ='https://rest.coinapi.io/v1/orderbooks/BITSTAMP_SPOT_'+ currency + '_' + base_currency + '/current?limit_levels=500'
        headers = {'X-CoinAPI-Key' : 'AC6546B4-0B1A-4F28-8579-9B3DC4634921'}
        response = requests.get(url, headers=headers)
        
        prices = []
        sizes=[]
        
        if response.status_code == 200:
            text = return_data_json(response.json()) 
            text = json.loads(text) 
            
            for i in range(len(text['bids'])):
                prices.append(text['bids'][i]['price'])
                sizes.append(text['bids'][i]['size'])
            date = text['time_exchange'][:10] + ' ' + text['time_exchange'][11:19] 
                    
        elif response.status_code == 400:
            print('UWAGA !!! ' , currency , ' nie występuje w bazie!')
            not_in_base.append(currency)
            
        elif response.status_code == 429:
            print('Nieprawidłowy klucz api !!!')
            
        else:
            print('Wystąpił bład ' , response.status_code , '!')
            
        if currency not in not_in_base:
            i = currencies.index(currency)
            data_dict[currency] = prices , sizes , date , amount[i]
    
    return data_dict 


def get_valuation(data_dict):
    
    valuation_data = {}
    total_value = 0
    
    for key in data_dict.keys():
        
        max_prices=[]
        max_sizes=[]
        
        prices = data_dict[key][0].copy()
        sizes = data_dict[key][1].copy()
        amount = data_dict[key][3]
        
        if sum(sizes) >= amount:
            while amount > 0:

                max_price = prices[0]
                max_size = sizes[0]
                
                max_prices.append(max_price)
                max_sizes.append(max_size)
                
                prices.pop(0)
                sizes.pop(0)
        
                amount = amount - float(max_size)
                
            max_sizes[-1] = max_sizes[-1] + amount
            
            valuation = np.sum(np.array(max_prices) * np.array(max_sizes))
            total_value += valuation
            valuation_data[key] = valuation
            
        else:
            print(key , '- zbyt mały zakres by wycenić taką ilosc zasobów! Zwiększ limit.') 
            
    return valuation_data , total_value


def count_profit(valuation_data , total_value , buy_prices , amount , base_currency):

    profit ={}
    
    for key in valuation_data.keys():
        i = list(valuation_data.keys()).index(key)
        profit[key] = valuation_data[key] - buy_prices[i] * amount[i] 
    
    total_profit = np.sum((list(profit.values())))
        
    return profit , total_profit               
        
            
    
def edit_wallet(file , data_list , currencies , amount):

    print('\n1 - usuń\n2 - dodaj\n3 - zmień ilość')
    action = input('Wprowadź akcję: ')
            
    if action == '1':
        
        del_currency = input('Wprowadź kryptowalutę, którą chcesz usunąć: ') 
        
        if del_currency in currencies:
            edit_data_list=[]
            for row in data_list:
                if row[0] != del_currency:
                    edit_data_list.append(row)
                    
            with open(file , 'w' , newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['WALUTA;ILOSC;CENA ZAKUPU USD [USD/szt.];CENA ZAKUPU EUR[EUR/szt.]']) 
                for row in edit_data_list:
                    csvwriter.writerow([row[0] + ';' + row[1] + ';' + row[2] + ';' + row[3]]) 
              
            csvfile.close()     
            print('Usunięto' , del_currency)                    
            
        else:
            print(del_currency , 'nie ma w portfelu!')
        
    elif action == '2':
    
        new_currency = input('Wprowadź nową kryptowalutę: ') 
    
        if new_currency not in currencies:
            new_amount = input('Wprowadź ilość (format np. 0.7): ')
            buy_price_USD = input('Wprowadź cenę zakupu (jednej krytpowaluty) w USD (format np. 0.7): ')
            buy_price_EUR = input('Wprowadź cenę zakupu (jednej krytpowaluty) w EUR (format np. 0.7): ')
            with open(file , 'a' , newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([new_currency + ';' + new_amount + ';' + buy_price_USD + ';' + buy_price_EUR])
                
            csvfile.close()
            print('Dodano' , new_currency , '!')
            
        else:
            print('Kryptowaluta istnieje w portfelu. Zmień jej ilość!')
            
    elif action == '3':
        
        currency = input('Wprowadź kryptowalutę do edycji: ') 
        
        if currency in currencies:
            new_amount = input('Wprowadź ilość (format np. 0.7): ')
            buy_price_USD = input('Wprowadź cenę zakupu (jednej krytpowaluty) w USD (format np. 0.7): ')
            buy_price_EUR = input('Wprowadź cenę zakupu (jednej krytpowaluty) w EUR (format np. 0.7): ')
            for row in data_list:
                if row[0] == currency:
                    i = data_list.index(row)
                    data_list[i][1] = new_amount
                    data_list[i][2] = buy_price_USD
                    data_list[i][3] = buy_price_EUR
                    
            with open(file , 'w' , newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['WALUTA;ILOSC;CENA ZAKUPU USD [USD/szt.];CENA ZAKUPU EUR[EUR/szt.]']) 
                for row in data_list:
                    csvwriter.writerow([row[0] + ';' + row[1] + ';' + row[2] + ';' + row[3]]) 
                    
            csvfile.close()
            print('Zmieniono ilosc' , currency , '!')
            
        else:
            print(currency , 'nie ma w portfelu. Dodaj do portfela!')
            

def main():
    #Dostępne waluty w api: BTC,LTC,ETH,XRP,BCH
    file = 'portfel.csv'
    base_currency = input('Wprowadź walutę bazową (USD,EUR): ')
    while base_currency not in ['EUR','USD']:
        base_currency = input('Wprowadź ponownie walutę bazową (USD,EUR): ')
    
    end = '1'
    
    while end == '1':
        
        print('\n                   MENU                   ')
        print('........................................')
        print('1. Wyswietl portfel\n2. Sprawdź wycenę kryptowalut.\n3. Sprawdź zysk.\n4. Edytuj portfel.\n5. Wyjscie')
        print('........................................')
        action = input('Wprowadź akcję: ')
        while action not in ['1','2','3','4' ,'5']:
            action = input('Wprowadź ponownie akcję: ')
            
        if action == '1':
            
            data_list , currencies , amount, buy_prices_USD , buy_prices_EUR = get_wallet(file)
            
            print('\n         Wyswietlanie portfela          ')
            print('........................................')
            print('Kryptowaluta' , '   Ilosc', 'Cena zakupu [USD/szt.]/[EUR/szt.]')
            print('........................................')
            for i in range(len(data_list)):
                print(data_list[i][0] , '           ' , data_list[i][1] , '       ' , data_list[i][2] + '/' + data_list[i][3])
            
        
        elif action == '2':
            
            data_list , currencies , amount , buy_prices_USD , buy_prices_EUR = get_wallet(file)
            data_dict = get_data(currencies , base_currency, amount) 
            valuation ,total_value= get_valuation(data_dict)
                
            print('\n..........Wycena kryptowalut..........')
            for key, value in valuation.items():
                print(key , round(value , 2) , base_currency)
            print('......................................')    
            print('W całym portfelu: ' , round(total_value , 2) , base_currency)
            print('......................................')
            
        elif action == '3':
                
            data_list , currencies , amount , buy_prices_USD , buy_prices_EUR = get_wallet(file)
            data_dict = get_data(currencies , base_currency, amount) 
            valuation_data ,total_value= get_valuation(data_dict)
            
            if base_currency == 'USD':
                buy_prices = buy_prices_USD
            else:
                buy_prices = buy_prices_EUR
                
            profit , total_profit = count_profit(valuation_data , total_value , buy_prices , amount , base_currency)
            print('\n................Zysk................')
            for key, value in profit.items():
                print(key , round(value , 2) , base_currency)
            print('......................................')    
            print('W całym portfelu: ' , round(total_profit , 2) , base_currency)
            print('......................................')
            
            
        elif action == '4':   
            
            stop_edition = '2'
            
            while stop_edition == '2':
                data_list , currencies , amount , buy_prices_USD , buy_prices_EUR = get_wallet(file)
                edit_wallet(file , data_list , currencies , amount)
                
                stop_edition = input('Czy chcesz zakończyć edycję? \n1 - tak\n2 - nie\nWprowadź akcję: ')
                while stop_edition not in ['1','2']:
                    stop_edition = input('Czy chcesz zakończyć edycję? \n1 - tak\n2 - nie\nWprowadź ponownie akcję: ')
                    
        elif action == '5':
            
            break
        
        end = input('Czy chcesz przejsc do menu?\n1 - tak\n2 - nie\nWprowadź akcję: ')
        while end not in ['1','2']:
            end = input('Czy chcesz przejsc do menu?\n1 - tak\n2 - nie\nWprowadź ponownie akcję: ')
            
    
main()