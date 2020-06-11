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
def trades_plot():
    title('Price - Amount Relation')
    plot(amount, color="green", label='Amount')
    plot(var, color="red", label='Price Var')
    xlabel('Days')
    tight_layout()
    legend(loc='lower right')
    savefig('Correlation.png')
    show()

trades_BTC = bitbay_trades()

amount = []
price = []
time = []
var = [0]


trades()
trades_plot()