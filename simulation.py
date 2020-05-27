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

month = len(prices) - 30

dates = dates[month:]
prices = prices[month:]



def Moving_avarage(data, days=30):
    new_data = data.copy()
    new_values = []
    for i in range(days):
        avg = np.sum(new_data) / len(new_data)
        new_data.pop(0)
        new_data.append(avg)
        new_values.append(avg)
    return new_values

def simulation(simulation = 100):

    simulated_data = []

    for i in range(simulation):

        data = Moving_avarage(prices)
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


predicted = Moving_avarage(prices)
simulated = simulation()

fig = plt.figure()

plt.subplot(2, 2, 1)
plt.plot(prices)
plt.title('Last month BTC prices')

plt.subplot(2, 2, 2)
plt.plot(predicted)
plt.title('Predicted prices for next month')

plt.subplot(2,2,3)
plt.plot(simulated)
plt.title('avarage from 100 simulations')


plt.show()


