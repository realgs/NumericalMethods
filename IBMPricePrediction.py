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
    xx = np.linspace(xdata.min()-3, xdata.max()+3, num=100)
    yy = normal(xx, xdata.mean(), xdata.std())
    plt.plot(xx,yy, color = 'red')
    plt.plot(xdata, np.zeros_like(xdata), 'o', markersize=5, alpha=0.1, color = 'blue')
    plt.title("normal distribution of the error in the model")
    plt.show()
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

API_KEY = 'ESJGNOSQE67NP8OM'
API = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=" + API_KEY

#extracting data 
data = API_call(API)['Time Series (Daily)']
dates = list(data.keys())
prices=[]
for i in range(len(dates)):
    prices.append(float(data[dates[i]]['4. close']))

#geting data for learning
d = '2012-05-04'#input("Give data in format: yyyy-mm-dd (max 20 yeras behind):")
d = dates.index(d)
N = len(prices)
xdata = np.array(prices[d:N-2])
ydata = np.array(prices[d+1:N-1])

#learning model
model = calculate_model(xdata, ydata)
a, mu, sigma = model

#ploting model
xx = np.linspace(xdata.min(), xdata.max(), 100)
yy = xx*a[1] + a[0]
plt.plot(xdata, ydata, 'ro')
plt.plot(xx,yy, color = 'yellow')
plt.plot(xx,yy+sigma, color = 'blue')
plt.plot(xx,yy-sigma, color = 'blue')
plt.title('MODEL')
plt.xlabel('price on previous day')
plt.ylabel('price on given day')
plt.legend(['data', 'Model', 'error standard deviation'])
plt.show()

#predicting 100 days ahead 
predicted_prices = simulation(prices[-1], model, 100)
plt.plot(predicted_prices)
plt.title("predicted prices for 100 days from one simulation \n" + "average="+str(np.mean(predicted_prices)) +"median="+ str(np.median(predicted_prices)) + "std="+str(np.std(predicted_prices)))
plt.show()

#100 simulations
predicted_sum = np.zeros_like(predicted_prices)
for i in range(100):
    predicted_prices = simulation(prices[-1], model, 100)
    predicted_sum += predicted_prices
predicted_avg = predicted_sum/100
plt.plot(predicted_avg)
plt.title("average predicted prices for 100 days from 100 simulations \n" + "average="+str(np.mean(predicted_avg)) +"median="+ str(np.median(predicted_avg)) + "std="+str(np.std(predicted_avg)))
plt.show()