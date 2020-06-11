import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

currency = ['BTC', 'DASH', 'GAME', 'LSK', 'LINK']

prices = {}

for i in currency:
    a = pd.read_csv('l5_data/' + i +'.csv')
    prices[i] = a.values.tolist()
    

for i in prices:
    for j in range(len(prices[i])):
        prices[i][j] = (prices[i][j][6])

prices_change = {}

for i in prices:
    prices_change[i] = []
    for j in range(len(prices[i])-1):
        prices_change[i].append( (prices[i][j+1] - prices[i][j]) /prices[i][j+1])

grow_sum = {}
drop_sum = {}

for i in prices_change:
    plt.plot(prices_change[i])
    sum_p = 0
    sum_m = 0
    for j in prices_change[i]:
        if j >= 0:
            sum_p += j
        else: 
            sum_m += j
    grow_sum[i] = sum_p
    drop_sum[i] = sum_m
 # najbardziej podatne na spadek/wzrost jest waluta o najwiekszej sumie procentów wzrostów/spadków   

for i in currency:
    if grow_sum[i] == max(grow_sum.values()):
        print('najwiekszy wzrost ' + i + str(grow_sum[i]))

    if drop_sum[i] == max(drop_sum.values()):
        print('najmniejszy spadek ' + i + str(drop_sum[i]))


plt.legend(currency)
plt.show()