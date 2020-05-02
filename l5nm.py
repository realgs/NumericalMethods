import requests as r
from matplotlib.pyplot import*
from scipy.stats import pearsonr

def trades():
    def json():
        response = r.get('https://bitbay.net/API/Public/BTC/trades.json')
        return response.json()

    trade=json()

    price=[]
    amount=[]
    variation=[0]
    time=[]

    for i in trade:
        price.append(i['price'])
        amount.append(i['amount'])
    
    for i in range(len(price)-1):
        variation.append(price[i+1] - price[i])
    
    correlation = pearsonr(variation, amount)
    
    
    
    title('BTC')
    plot(amount, label="amount")
    plot(variation, label="variation")
    xlabel('Days')
    savefig('plot.png')
    legend(loc="upper left")
    show()
    
    print("correlation: ",correlation)

trades()    