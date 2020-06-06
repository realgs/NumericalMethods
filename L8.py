import requests
import numpy as np
import matplotlib.pyplot as plt
import json


def API_DATA():

    request = requests.get\
    ('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=DQHTDT7WB9NVTARN')
    request = request.json()
    data = json.dumps(request, sort_keys=(True), indent=4)
    data = json.loads(data)
    return data

data = API_DATA()['Time Series (Digital Currency Daily)']

keys = list(data.keys())

prices=[]
dates = []

#getting the last 30 days
for i in range(len(keys)):
    prices.append(float(data[keys[i]]['4a. close (USD)']))

for keys,items in data.items():
    dates.append(keys)

learning_from = len(prices) - (249 + 153)

real_values = len(prices) - (249)

dates = dates[real_values:]

prices_real = prices[real_values:]

prices = prices[learning_from:]

def Moving_average(data, days=30):
    new_data = data.copy()
    new_values = []
    for i in range(days):
        avg = np.sum(new_data) / len(new_data)
        new_data.pop(0)
        new_data.append(avg)
        new_values.append(avg)
    return new_values

def simulation(prices,simulation = 100):

    simulated_data = []

    for i in range(simulation):

        data = Moving_average(prices, days=249)
        simulated_data.append(data)

    simulated_result = []
    for i in range(len(simulated_data[0])):

        index_values = []

        for j in range(len(simulated_data)):

            index = simulated_data[j][i]
            index_values.append(index)

        avarage = np.sum(index_values) / len(index_values)
        simulated_result.append(avarage)

    return simulated_result


For_simulation = prices.copy()
simulated_100 = simulation(For_simulation)
simulated_data = Moving_average(For_simulation, days=249)

fig = plt.figure()

plt.subplot(2, 2, 1)
plt.plot(prices_real)
plt.title('Btc prices from 10.2019 to 05.2020')

plt.subplot(2, 2, 2)
plt.plot(simulated_data)
plt.title('Predicted prices for the same period')

plt.subplot(2,2,3)
plt.plot(simulated_100)
plt.title('average from 100 simulations')


plt.show()