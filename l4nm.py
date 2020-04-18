import requests as r
from matplotlib.pyplot import*
from datetime import datetime

def trades():
    def json():
        response = r.get('https://bitbay.net/API/Public/BTCPLN/trades.json')
        return response.json()

    trade=json()

    date_sell=[]
    price_sell=[]
    date_buy=[]
    price_buy=[]
    time_buy=[]
    time_sell=[]
    extreme_buy=[]
    extreme_sell=[]
    ex_buy=[]
    ex_sell=[]
    
    for i in range(50):
        if trade[i]['type']=='buy':
            price_buy.append(trade[i]['price'])
            date_buy.append(trade[i]['date'])
        else: 
            price_sell.append(trade[i]['price'])
            date_sell.append(trade[i]['date'])


    for i in range(len(date_buy)):
        time_buy.append(datetime.fromtimestamp(date_buy[i]))

    for i in range(len(date_sell)):
        time_sell.append(datetime.fromtimestamp(date_sell[i]))
    
    j=1
    for j in range(len(price_buy)-1):
        
        if price_buy[j]>price_buy[j-1] and price_buy[j]>price_buy[j+1]:
            extreme_buy.append(time_buy[j])
            ex_buy.append(price_buy[j])
        
        elif price_buy[j]<price_buy[j-1] and price_buy[j]<price_buy[j+1]:
            extreme_buy.append(time_buy[j])
            ex_buy.append(price_buy[j])
    j=1
    for j in range(len(price_sell)-1):
        
        if price_sell[j]>price_sell[j-1] and price_sell[j]>price_sell[j+1]:
            extreme_sell.append(time_sell[j])
            ex_sell.append(price_sell[j])
        
        elif price_sell[j]<price_sell[j-1] and price_sell[j]<price_sell[j+1]:
            extreme_sell.append(time_sell[j])
            ex_sell.append(price_sell[j])
        
        

    
    title('price buy BTCPLN')
    plot(time_buy,price_buy)
    plot(extreme_buy,ex_buy,'bo')
    show()
    title('price sell BTCPLN')
    plot(time_sell,price_sell)
    plot(extreme_sell,ex_sell,'bo')
    show()
    
trades()    
