import requests 
import json
import numpy as np
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

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
    date_sell=dict_data_sell['date'].copy()
    date_buy=dict_data_buy['date'].copy()
    for i in range(len(date_sell)):
        conv_date_sell=datetime.fromtimestamp(date_sell[i])
        date_sell[i]=conv_date_sell.strftime("%d %b %Y \n %H:%M")
    for i in range(len(date_buy)):
        conv_date_buy=datetime.fromtimestamp(date_buy[i])
        date_buy[i]=conv_date_buy.strftime("%d %b %Y \n %H:%M")
    date_sell.reverse()   
    date_buy.reverse()
    return date_sell,date_buy


def count_indicators(dict_data,converted_dates,atributes):
    indicators_atribute_data={}
    for j in range(len(atributes)):
        indicators_type_data={}
        for i in range(len(dict_data)):
            trade_type=' SELL' if i==0 else ' BUY'
            indicators_date=converted_dates[i]
            data_atribute=dict_data[i][atributes[j]]
            sum_atribute=sum(data_atribute)
            aver_val=sum_atribute/len(data_atribute)
            array_aver_val=aver_val*np.array(len(data_atribute)*[1])
            std_dev=np.std(data_atribute)
            array_std_up=array_aver_val+std_dev
            array_std_down=array_aver_val-std_dev
            absolute_growth=[0]
            time_growth=[0]
            for index in range(len(data_atribute)-1):
                if dict_data[i]['date'][index+1]-dict_data[i]['date'][index]!=0:
                    t_g=(data_atribute[index+1]-data_atribute[index])/(dict_data[i]['date'][index+1]-dict_data[i]['date'][index])
                else:
                    t_g=(data_atribute[index+1]-data_atribute[index])
                a_g=data_atribute[index+1]-data_atribute[index]
                absolute_growth.append(a_g)
                time_growth.append(t_g)
            indicators_type_data[trade_type]=[indicators_date,array_aver_val,array_std_up,array_std_down,absolute_growth,time_growth]
        indicators_atribute_data[atributes[j]]=indicators_type_data
    return indicators_atribute_data


def count_extremes(dict_data,converted_dates,atributes):
    extremes_atribute_data={}
    for j in range(len(atributes)):
        extremes_type_data={}
        for i in range(len(dict_data)):
            trade_type=' SELL' if i==0 else ' BUY'
            array_atribute=np.array(dict_data[i][atributes[j]])
            index_max_atribute=argrelextrema(array_atribute, np.greater)[0]
            index_min_atribute=argrelextrema(array_atribute, np.less)[0]
            max_atribute=array_atribute[index_max_atribute]
            min_atribute=array_atribute[index_min_atribute]
            extremes=np.concatenate((min_atribute,max_atribute),axis=None)
            index_extremes=np.concatenate((index_min_atribute,index_max_atribute),axis=None)
            extremes_date=[]
            for index in index_extremes:
                ex_date=converted_dates[i][index]
                extremes_date.append(ex_date)
            extremes_type_data[trade_type]=[extremes_date,extremes]
        extremes_atribute_data[atributes[j]]=extremes_type_data
    return extremes_atribute_data
                    
    
def print_plots(dict_data,converted_dates,atributes,extrema_atribute_data,indicators_value):
    m=0
    for j in range(len(atributes)):
        extrema_type_data=extrema_atribute_data[atributes[j]]
        indicators_type_data=indicators_value[atributes[j]]
        for i in range(len(dict_data)):
            m+=1
            trade_type=' SELL' if i==0 else ' BUY'
            extremes_data=extrema_type_data[trade_type]
            indicators_data=indicators_type_data[trade_type]
            plt.subplot(4,1,m)
            plt.plot(converted_dates[i],dict_data[i][atributes[j]],'-o',label=atributes[j]+trade_type)
            plt.plot(extremes_data[0],extremes_data[1],'o',color='black',label='extremes')
            plt.plot(indicators_data[0],indicators_data[1],color='black',label='average value')
            plt.plot(indicators_data[0],indicators_data[2],color='green',label='standard deviation')
            plt.plot(indicators_data[0],indicators_data[3],color='green')
            plt.plot(indicators_data[0],indicators_data[4],'-o',color='orange',label='absolute_growth')
            plt.plot(indicators_data[0],indicators_data[5],'-o',color='purple',label='time_growth')
            fig = plt.gcf()
            fig.set_size_inches(20, 30)
            plt.title(atributes[j]+trade_type+' [USD]',size=20)
            plt.xlabel('date',size=15)
            plt.ylabel(atributes[j],size=15)
            plt.legend(prop={'size': 10})
          

def main(atributes):  
    atributes=list(atributes)
    response = requests.get("https://bitbay.net/API/Public/BTC/trades.json?sort=desc")
    if response.status_code==200:
        dict_data=dict_trades_data(response,['date']+atributes)
        converted_dates=conv_date(dict_data)
        indicators_value=count_indicators(dict_data,converted_dates,atributes)
        extremes_atribute_data=count_extremes(dict_data,converted_dates,atributes)
        print_plots(dict_data,converted_dates,atributes,extremes_atribute_data,indicators_value) 
    else:
        print('Wystąpił błąd !')
main(['price','amount'])