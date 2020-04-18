import requests
from matplotlib.pyplot import *
from datetime import datetime


def bitbay_trades():

    response = requests.get("https://bitbay.net/API/Public/BTCPLN/trades.json")

    return response.json()

def trades():
    
    for i in range (49):
        
        if trades_BTC_PLN[i]['type'] == 'buy':
            date_buy.append(trades_BTC_PLN[i]['date'])
            price_buy.append(trades_BTC_PLN[i]['price'])
            
        elif trades_BTC_PLN[i]['type'] == 'sell':
            date_sell.append(trades_BTC_PLN[i]['date'])
            price_sell.append(trades_BTC_PLN[i]['price'])
            
    for i in range(len(date_buy)):
        time_buy.append(datetime.fromtimestamp(date_buy[i]))
        
    for i in range(len(date_sell)):
        time_sell.append(datetime.fromtimestamp(date_sell[i]))
        
     
    i=1
    for i in range(len(price_buy)-1):
        if price_buy[i] < price_buy[i-1] and price_buy[i] < price_buy[i+1]:
            ex_buy.append(price_buy[i])
            point_buy.append(time_buy[i])
        elif price_buy[i] > price_buy[i-1] and price_buy[i] > price_buy[i+1]:
            ex_buy.append(price_buy[i])
            point_buy.append(time_buy[i])
    
    
    i=1
    for i in range(len(price_sell)-1):
        if price_sell[i] < price_sell[i-1] and price_sell[i] < price_sell[i+1]:
            ex_sell.append(price_sell[i])
            point_sell.append(time_sell[i])
        elif price_sell[i] > price_sell[i-1] and price_sell[i] > price_sell[i+1]:
            ex_sell.append(price_sell[i])
            point_sell.append(time_sell[i])
    
    
def trades_buy():
    title('Buy Price BTC_PLN')
    plot(time_buy, price_buy)
    plot(point_buy,ex_buy, 'r*', label='extreme')
    legend(loc='upper right')
    show()
        
def trades_sell():
    title('Sell Price BTC_PLN')
    plot(time_sell, price_sell)
    plot(point_sell,ex_sell, 'r*', label='extreme')
    legend(loc='upper right')
    show()

trades_BTC_PLN = bitbay_trades()

date_buy = []
price_buy = []
time_buy = []
ex_buy = []
point_buy = []

date_sell = []
price_sell = []
time_sell = []
ex_sell = []
point_sell = []
  

trades()
trades_buy()
trades_sell()