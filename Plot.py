import requests
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation

response = requests.get('https://bitbay.net/API/Public/BTCUSD/trades.json?sort=asc')
prices=[]
for i in response.json():
    prices.append(i)


x_vals=[]
y_vals=[]
index=0

for i in range(len(prices)):
    index+=1
    x_vals.append(index)
    y_vals.append(prices[i]['price'])



def new_prices():
    global prices
    response = requests.get('https://bitbay.net/API/Public/BTCUSD/trades.json?sort=asc')
    prices_n=[]
    for i in response.json():
        prices_n.append(i)
    n=[]
    for i in prices_n:
        if i['date']>prices[-1]['date']:
            print(i['date'])
            n.append(i)
    for i in n:
        prices.append(i)
        print(i)
    return n

y_vals.pop()
x_vals.pop()
prices.pop()

def avg(num):
    sum=0
    for i in num:
        sum+=i
    return sum/len(num)


def animate(i):
    global index
    n_p = new_prices()
    if len(n_p)>0:
        for i in n_p:
            index+=1
            x_vals.append(index)
            y_vals.append(i['price'])

    przeg_x=[]
    przeg_y=[]
    for i in range(len(y_vals)-2):
        if (y_vals[i]<y_vals[i+1]>y_vals[i+2]) or (y_vals[i]>y_vals[i+1]<y_vals[i+2]):
            przeg_x.append(i+2)
            przeg_y.append(y_vals[i+1])

    average = avg(y_vals)
    maxi = max(y_vals)
    mini = min(y_vals)
    avg_vals=[]
    max_vals=[]
    min_vals=[]
    for i in x_vals:
        avg_vals.append(average)
        max_vals.append(maxi)
        min_vals.append(mini)
    plt.cla()
    plt.plot(x_vals, y_vals, label='Price')
    plt.plot(x_vals, avg_vals, label='Average Price')
    plt.plot(x_vals, max_vals, label='Max Price')
    plt.plot(x_vals, min_vals, label='Min Price')
    plt.plot(przeg_x,przeg_y,'o',label='Inflection points')
    plt.legend()
ani = FuncAnimation(plt.gcf(), animate,10000)
plt.tight_layout()

plt.show()
