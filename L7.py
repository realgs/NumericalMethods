from datetime import datetime, timezone

import matplotlib.pyplot as pyplot
import numpy
import pandas
import requests

values = []
dates = []


def main():
    print("Numerical Methods assignment L7 kalamek")
    baseCurrency = input("Select base currency (USD, EUR): ").lower()
    cryptoCurrency = input("Select crypto currency (BTC, ETH, BCH, etc.): ").lower()
    startDateRaw = input("Insert start date (DD-MM-YYYY): ")
    multiPassCount = int(input("How many passes should multiple simulation take: "))

    dt = datetime.strptime(startDateRaw, "%d-%m-%Y")
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

    json = downloadData(baseCurrency, cryptoCurrency, timestamp)
    parseData(json)

    single = predict()
    printSingleStatistics(single)

    multi = multiple(multiPassCount)
    printMultiStatistics(multi)

    plot(multi, single)


def downloadData(baseCurrency, cryptoCurrency, timestamp):
    json = requests.get(
        f"https://www.bitstamp.net/api/v2/ohlc/{cryptoCurrency}{baseCurrency}/?"
        f"step=86400&"
        f"limit=1000&"
        f"start={int(timestamp)}"
    ).json()
    return json


def parseData(json):
    data = json['data']
    ohlc = data['ohlc']
    for i in range(len(ohlc)):
        values.append(float(ohlc[i]['close']))
        dates.append(datetime.fromtimestamp(int(ohlc[i]['timestamp'])))


def printSingleStatistics(single):
    print("\nSingle pass:")
    print(f"Average: {numpy.mean(single)}")
    print(f"Standard deviation: {numpy.std(single)}")
    print(f"Median: {numpy.median(single)}\n")


def printMultiStatistics(multi):
    print("Multi pass:")
    print(f"Average: {numpy.mean(multi)}")
    print(f"Standard deviation: {numpy.std(multi)}")
    print(f"Median: {numpy.median(multi)}\n")


def plot(multi, single):
    pyplot.subplot(3, 1, 1)
    pyplot.xticks(rotation=30)
    pyplot.plot(dates, values, '-o', label='predicted prices')

    pyplot.subplot(3, 1, 2)
    pyplot.xticks(rotation=30)
    pyplot.plot(dates, single, '-o')

    pyplot.subplot(3, 1, 3)
    pyplot.xticks(rotation=30)
    pyplot.plot(dates, multi, '-o')

    pyplot.show()


def multiple(count):
    predictions = []

    for i in range(count):
        predictions.append(predict())

    average = []
    for i in range(len(predictions[0])):
        entries = []
        for j in range(len(predictions)):
            entries.append(predictions[j][i])
        average.append(numpy.mean(entries))

    return average


# TODO: refactor
def predict():
    localValues = values.copy()
    prediction = []

    for i in range(len(localValues)):
        increase = []
        decrease = []

        calculateTrend(decrease, increase, localValues)

        noise = getNoise()
        predicted = getPrediction(decrease, increase, noise)
        prediction.append(predicted)

        localValues.append(predicted)
        localValues = localValues[1:]

    return prediction


def calculateTrend(decrease, increase, localValues):
    for j in range(1, len(localValues)):
        d = abs((localValues[j] - localValues[j - 1]) / localValues[j])
        if d > 0:
            increase.append(d)
        else:
            decrease.append(d)


def getNoise():
    return abs(numpy.random.choice(pandas.DataFrame(numpy.random.normal(1, 1 / 3, 100))[0]))


def getPrediction(decrease, increase, noise):
    return values[-1] * ((1 if len(decrease) / len(increase) >= 1 else -1) - numpy.std(increase) * noise)


main()