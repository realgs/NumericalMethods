import requests
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


def correlation():
    response = (requests.get("https://bitbay.net/API/Public/BTC/Trades.json?sort=asc")).json()

    prices = []
    amounts = []
    price_variation = [0]

    for item in response:
        prices.append(item['price'])
        amounts.append(item['amount'])

    for i in range(len(prices) - 1):
        price_variation.append(prices[i+1] - prices[i])

    corr, _ = pearsonr(price_variation, amounts)

    plt.plot(price_variation, label="Price")
    plt.plot(amounts, label="Amount")
    plt.legend()
    plt.title("Pearson's coefficient {}".format(corr))
    plt.xlabel('Days')
    plt.ylabel('Value')
    plt.savefig('correlation.png')
    plt.show()

    return corr


print('Correlation coefficient indicates that there is a positive correlation but its weak and likely unimportant: {}'.format(correlation()))
