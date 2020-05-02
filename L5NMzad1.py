import requests
from matplotlib.pyplot import *
from scipy.stats import pearsonr



def bitbay_trades():

    response = requests.get("https://bitbay.net/API/Public/BTC/trades.json")

    return response.json()

def trades():

    for i in range (49):
        price.append(trades_BTC[i]['price'])
        amount.append(trades_BTC[i]['amount'])
        
    for i in range(49):
        time.append(i)
        
    for i in range(48):
        var.append(price[i+1]-price[i])
        
    corre = pearsonr(var, amount)
    print("Pearson correlation",corre)
        

def trades_plot():
    title('Price - Amount Relation')
    plot(amount, label='Amount')
    plot(var, label='Price Var')
    xlabel('Days')
    legend(loc='upper left')
    savefig('Pearson_Correlation.png')
    show()


trades_BTC = bitbay_trades()

amount = []
price = []
time = []
var = [0]


trades()
trades_plot()