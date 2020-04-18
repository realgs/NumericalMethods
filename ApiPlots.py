import requests 
import json
from datetime import datetime

def return_data_json(obj):
    text = json.dumps(obj,sort_keys=(True), indent = 4)
    return text

def dict_trades_data(response,atributes):    
    json_data= return_data_json(response.json()) 
    to_dict = json.loads(json_data)
    dict_data_sell={}
    dict_data_buy={}
    dict_data=dict_data_sell,dict_data_buy
    for j in range(len(atributes)):
        atribute_list_sell=[]
        atribute_list_buy=[]
        for i in range(len(to_dict)):
            atribute_list=(atribute_list_sell if to_dict[i]['type']=='sell' else atribute_list_buy)
            data=to_dict[i][atributes[j]]
            atribute_list.append(data)
        dict_data_sell[atributes[j]]=atribute_list_sell
        dict_data_buy[atributes[j]]=atribute_list_buy
    return dict_data

def conv_date(dict_data):
    dict_data_sell,dict_data_buy=dict_data
    date_sell=dict_data_sell['date']
    date_buy=dict_data_buy['date']
    for i in range(len(date_sell)):
        conv_date_sell=datetime.fromtimestamp(date_sell[i])
        date_sell[i]=conv_date_sell.strftime("%d %b %Y \n %H:%M")
    for i in range(len(date_buy)):
        conv_date_buy=datetime.fromtimestamp(date_buy[i])
        date_buy[i]=conv_date_buy.strftime("%d %b %Y \n %H:%M")
    date_sell.reverse()   
    date_buy.reverse()
    return date_sell,date_buy



def main(atributes):   
    response = requests.get("https://bitbay.net/API/Public/BTC/trades.json?sort=desc")
    if response.status_code==200:
        dict_data=dict_trades_data(response,['date']+atributes)
        converted_dates=conv_date(dict_data)
    else:
        print('Wystąpił błąd !')
main(['price','amount'])
   