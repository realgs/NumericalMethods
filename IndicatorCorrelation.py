import requests as rq
import matplotlib.pyplot as plt
import json

response = rq.get("https://bitbay.net/API/Public/BTC/trades.json")

def json_to_str(obj):
        text = json.dumps(obj,sort_keys=(True), indent = 4) 
        x = json.loads(text)
        return x


a = json_to_str(response.json())
price = []
amount = []


for i in range(len(a)):
    price.append(a[i]['price'])
    amount.append(a[i]['amount'])


price = price[::-1]
amount = amount[::-1]

price_change = [0]

for i in range(len(price)-1):
    price_change.append(price[i+1]-price[i])

# współczynnik korelacji Pearsona
pc_s = sum(price_change)
a_s = sum(amount)

pca_s = 0
sq_pc_s = 0
sq_a_s = 0
for i in range(len(price_change)):
    pca_s = pca_s + (price_change[i] * amount[i])
    sq_pc_s = sq_pc_s + price_change[i]**2
    sq_a_s = sq_a_s + amount[i]**2

correlation = ( len(price_change) * pca_s - pc_s * a_s)/(((len(price_change)*sq_pc_s-pc_s**2)*(len(amount)*sq_a_s-a_s**2))**(1/2))

#plot to png
plt.plot(price_change)
plt.plot(amount)
plt.title('correlation coefficient = ' + str(correlation))
plt.legend(['price change', 'amount'])
plt.savefig('correlation.png')
plt.show()