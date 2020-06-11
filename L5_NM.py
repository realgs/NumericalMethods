import requests
import matplotlib.pyplot as plt
import numpy as np

def bitbay_BTC_trades():
    response = requests.get('https://bitbay.net/API/Public/BTC/trades.json')

    return response.json()

btc = bitbay_BTC_trades()

price = []
amount = []

for i in range(len(btc)):
    price.append(btc[i]['price'])
    amount.append(btc[i]['amount'])

price_change = []
for i in range(len(price)-1):
    variable = price[i+1] - price[i]
    price_change.append(variable)

price_avg = sum(price_change) / len(price_change)
amount_avg = sum(amount) / len(amount)

SDx = 0
SDy = 0

variable_x = []

for i in range(len(price_change)):

    equ = (price_change[i] - price_avg) ** 2
    variable_x.append(equ)

variable_x = sum(variable_x)

SDx = np.sqrt(variable_x / len(price))

variable_y = []

for i in range(len(amount)):
    y = (amount[i] - amount_avg) ** 2
    variable_y.append(y)

variable_y = sum(variable_y)

SDy = np.sqrt(variable_y / len(amount))

Cov_xy = 0

Cov = []
for i in range(len(price_change)):
    summing = (price_change[i] - price_avg) * (amount[i] - amount_avg)
    Cov.append(summing)

Cov_xy = sum(Cov) / len(price)

Pearson_correlation = Cov_xy / (SDx * SDy)

Linear_determination_indicator = (Pearson_correlation ** 2) * 100

file = open('Pearson_correlation.txt', 'w')
file.write('Cearson correlation between price and amount sold for BTC is equal to :')
file.write(str(Pearson_correlation))
file.write('\n Linear determination indicator :')
file.write(str(Linear_determination_indicator))
file.write(' %')

plt.plot(price_change, label ='price change')
plt.plot(amount, label = 'amount')
plt.title("Pearsons's correlation: {}".format(Pearson_correlation))
plt.savefig("Pearson_correlation.png")
plt.show()


