import requests as rq
import json
import matplotlib.pyplot as plt
import numpy as np

#calling api for data
def API_call(obj): 
    obj = rq.get(obj).json()
    text = json.dumps(obj,sort_keys=(True), indent = 4) 
    x = json.loads(text)
    return x

#least squares method
def regresion(xdata, ydata): 
    if len(xdata.shape) == 1:
        xN = 1
    else:
        xN = xdata.shape[0] 
    yN = 1
    X = xdata.reshape(xN,-1)
    Y = ydata.reshape(yN,-1)
    X = np.vstack([np.ones_like(X[0]), X])
    a = np.linalg.inv(X@X.T) @X@Y.T
    a = np.vstack([a])
    Y_pr = a.T @ X
    return (a, Y_pr) 

#most likelyhood estimation
def MLE(xdata): 
    normal = lambda x, mu, sig : np.exp(-(x-mu)**2/(2*sig**2))/(sig*np.sqrt(2*np.pi))
    return  (xdata.mean(), xdata.std())

#calculating model parameters
def calculate_model(xdata, ydata):
    a, err = regresion(xdata, ydata)
    err = (ydata - err) 
    mu, sigma = MLE(err)
    return(a, mu, sigma)

#prediction will be the value  of a linear model a[1]*x + a[0], plus randolmly generated error from normal distribiution with given mu and sigma
def prediction(x, model): 
    a, mu, sigma = model
    return a[1]*x+a[0]+np.random.normal(loc = mu, scale = sigma)

#simulation for n days
def simulation(x0, model, n):
    predicted_prices = list(prediction(x0, model))
    for i in range(n-1):
        predicted_prices.append(prediction(predicted_prices[-1], model))
    return predicted_prices

def error(a,b):
    err = 0
    for i in range(len(a)):
        err+=(b[i]-a[i])**2
    return (err)

API_KEY = 'ESJGNOSQE67NP8OM'
API = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=" + API_KEY

#extracting data 
data = API_call(API)['Time Series (Daily)']
dates = list(data.keys())
prices=[]
for i in range(len(dates)):
    prices.append(float(data[dates[i]]['4. close']))

#geting data for learning
d = '2019-01-02'
d = dates.index(d)
N = len(prices)
days = N-d
xdata = np.array(prices[0:d])
ydata = np.array(prices[1:d+1])

#learning model
model = calculate_model(xdata, ydata)
a, mu, sigma = model

#real data
real_data = prices[d:]
plt.plot(real_data)

#predicting 
predicted_prices = simulation(prices[-1], model, days)
plt.plot(predicted_prices)
plt.legend(['real data', 'prediction'])
plt.show()

print(error(predicted_prices, real_data))

#100 simulations
predicted_sum = np.zeros_like(predicted_prices)
for i in range(100):
    predicted_prices = simulation(prices[-1], model, days)
    predicted_sum += predicted_prices
predicted_avg = predicted_sum/100
plt.title("100 simulations")
plt.plot(predicted_avg)

plt.show()
print(error(predicted_avg, real_data))
