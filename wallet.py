import csv
import requests
import json
import pytz
import numpy as np
import matplotlib.pyplot as plt
import datetime


def get_wallet(file):
    
    with open(file , newline='') as csvfile:       
        data = csv.reader(csvfile, delimiter=';')
        data_list = list(data)
        data_list = data_list[1:]
        currencies = []
        amount = []
        
        for row in data_list:         
            currencies.append(row[0])
            amount.append(row[1])
            
    csvfile.close()
            
    return data_list , currencies , amount



def return_data_json(obj):
    
    text = json.dumps(obj,sort_keys=(True), indent = 4)
    
    return text



def get_data(currencies ,  base_currency , time_start , time_end , amount):
    
    data_dict={}
    not_in_base=[]
    
    for currency in currencies:
        
        url = 'https://rest.coinapi.io/v1/trades/BITSTAMP_SPOT_' + currency + '_' +  base_currency + '/history?time_start=' + time_start +'&time_end=' + time_end + '&limit=1000' 
        headers = {'X-CoinAPI-Key' : '39C9010B-734C-4E96-85AC-D2425C7904CC'}
        response = requests.get(url, headers=headers)
        
        prices = []
        sizes=[]
        dates = []
        
        if response.status_code == 200:
            text = return_data_json(response.json())
            text = json.loads(text) 
            for i in range(len(text)):
                if text[i]['taker_side'] == 'BUY':
                    prices.append(text[i]['price'])
                    sizes.append(text[i]['size'])
                    dates.append(text[i]['time_exchange'][11:13] + '\n' + text[i]['time_exchange'][14:19])
                    
        elif response.status_code == 400:
            print('UWAGA !!! ' , currency , ' nie występuje w bazie!')
            not_in_base.append(currency)
            
        elif response.status_code == 429:
            print('Nieprawidłowy klucz api !!!')
            
        else:
            print('Wystąpił bład ' , response.status_code , '!')
            
        if currency not in not_in_base:
            i = currencies.index(currency)
            data_dict[currency] = prices , sizes , dates , float(amount[i])
    
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

                max_price = max(prices)
                index_max_price = prices.index(max_price)
                max_size = sizes[index_max_price]
                
                max_prices.append(max_price)
                max_sizes.append(max_size)
                
                prices.pop(index_max_price)
                sizes.pop(index_max_price)
        
                amount = amount - float(max_size)
                
            max_sizes[-1] = max_sizes[-1] + amount
            
            valuation = np.sum(np.array(max_prices) * np.array(max_sizes))
            total_value += valuation
            valuation_data[key] = valuation
            
        else:
            print(key , '- zbyt mały zakres czasu by wycenić taką ilosc zasobów! Zwiększ zakres czasu.')      
            
    return valuation_data , total_value




def plot_changes(data_dict , base_currency):
    
    atributes = ['price' , 'amount']
    i=0
    
    fig, ax = plt.subplots(len(atributes) * len(data_dict.keys()) , 1)
    
    for key in data_dict.keys():
        for a in range(len(atributes)):
            ax[i].plot(data_dict[key][2] , data_dict[key][a] , '-o')
            ax[i].set_title(key)
            ax[i].set_xlabel('Data')
            ax[i].set_ylabel(atributes[a] + ' ' + key + ' [' + base_currency + ']')
            fig = plt.gcf()
            fig.set_size_inches(35, 20)
            i += 1
        
    plt.show()
            
    
def edit_wallet(file , data_list , currencies , amount):

    print('\n1 - usuń\n2 - dodaj\n3 - zmień ilość')
    action = input('Wprowadź akcję: ')
            
    if action == '1':
        
        del_currency = input('Wprowadź walutę, którą chcesz usunąć: ') 
        
        if del_currency in currencies:
            edit_data_list=[]
            for row in data_list:
                if row[0] != del_currency:
                    edit_data_list.append(row)
                    
            with open(file , 'w' , newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['WALUTA;ILOSC']) 
                for row in edit_data_list:
                    csvwriter.writerow([row[0] + ';' + row[1]]) 
              
            csvfile.close()     
            print('Usunięto' , del_currency)                    
            
        else:
            print(del_currency , 'nie ma w portfelu!')
        
    elif action == '2':
    
        new_currency = input('Wprowadź nową walutę: ') 
    
        if new_currency not in currencies:
            new_amount = input('Wprowadź ilość (format np. 0.7): ')
            with open(file , 'a' , newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([new_currency + ';' + new_amount])
                
            csvfile.close()
            print('Dodano' , new_currency , '!')
            
        else:
            print('Waluta istnieje w portfelu. Zmień jej ilość!')
            
    elif action == '3':
        
        currency = input('Wprowadź walutę do edycji: ') 
        
        if currency in currencies:
            new_amount = input('Wprowadź ilość (format np. 0.7): ')
            for row in data_list:
                if row[0] == currency:
                    i = data_list.index(row)
                    data_list[i][1] = new_amount
                    
            with open(file , 'w' , newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['WALUTA;ILOSC']) 
                for row in data_list:
                    csvwriter.writerow([row[0] + ';' + row[1]]) 
                    
            csvfile.close()
            print('Znieniono ilosc' , currency , '!')
            
        else:
            print(currency , 'nie ma w portfelu. Dodaj do portfela!')
            
def get_time():
    
    while True:
      try:
         time_range = int(input('Wprowadź zakres (w minutach): '))       
      except ValueError:
         print('Wprowadź wartosc liczbową!!!')
         continue
      else:
         break

    tz = pytz.timezone('UTC')
    time_end = datetime.datetime.now(tz)
    time_start = time_end - datetime.timedelta(minutes = time_range)
        
    time_end = str(time_end)[:10] + 'T' + str(time_end)[11:19]
    time_start = str(time_start)[:10] + 'T' + str(time_start)[11:19]

    return time_start , time_end
            

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
        print('1. Wyswietl portfel\n2. Sprawdź wycenę zasobów.\n3. Wyswietl wykresy cen i ilosci.\n4. Edytuj portfel.\n5. Wyjscie')
        print('........................................')
        action = input('Wprowadź akcję: ')
        while action not in ['1','2','3','4','5']:
            action = input('Wprowadź ponownie akcję: ')
            
        if action == '1':
            
            data_list , currencies , amount = get_wallet(file)
            
            print('\n         Wyswietlanie portfela          ')
            print('........................................')
            print('Waluta' , '            Ilosc')
            print('........................................')
            for i in range(len(data_list)):
                print(data_list[i][0] , '              ' , data_list[i][1])
            
        
        elif action == '2':
            
            time_start , time_end = get_time()
            data_list , currencies , amount = get_wallet(file)
            data_dict = get_data(currencies , base_currency , time_start , time_end, amount) 
            valuation ,total_value= get_valuation(data_dict)
                
            print('\n..........Wycena kryptowalut..........')
            for key, value in valuation.items():
                print(key , round(value , 2) , base_currency)
            print('......................................')    
            print('W całym portfelu: ' , round(total_value , 2) , base_currency)
            print('......................................')
            
        elif action == '3':
            
            time_start , time_end = get_time()
            print('\n..........Trwa wyswietlanie..........\n\nUWAGA!!! Data podana w UTC.')
            data_list , currencies , amount = get_wallet(file)
            data_dict = get_data(currencies , base_currency , time_start , time_end, amount) 
            plot_changes(data_dict , base_currency)
            
        elif action == '4':   
            
            stop_edition = '2'
            
            while stop_edition == '2':
                data_list , currencies , amount = get_wallet(file)
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