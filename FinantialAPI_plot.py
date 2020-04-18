from FinancialAPI import connect_API
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from os import path
import pandas as pd
import sys


def download_data(upd_idx=None, responses=None):
    params = [['BTC', 'USD'], 'trades']
    url = "https://bitbay.net/API/Public/"
    if upd_idx:
        print("UPDATING DATABASE...")
        responses_n = connect_API(url, params, None, upd_idx)
        while len(responses_n) % 50 == 0 and len(responses_n) > 0:
            try:
                responses_n.extend(connect_API(url, params, None, since=int(responses_n[-1].get("tid"))))
            except:
                print('RECONECTING...')
                responses_n = pd.DataFrame(responses_n)
                responses = pd.concat([responses, responses_n], ignore_index=True)
                save_data(responses)
                responses = load_data()
                update(responses)
        print("UPDATE COMPLETED (updated {} rows)".format(int(responses_n[-1].get("tid")) - upd_idx)) if len(
            responses_n) > 0 else print("Nothing to update!")
        if len(responses_n) > 0:
            responses_n = pd.DataFrame(responses_n)
            responses = pd.concat([responses, responses_n], ignore_index=True)
        else:
            return responses
    else:
        total = connect_API(url, params, None, None, 'desc')
        total = int(total[0]['tid']) + 1
        responses = connect_API(url, params, )
        print("Downloading data...\nIt will take about 10-15 minutes!!")
        while len(responses) % 50 == 0:
            try:
                # print(responses[-1].get("tid"))
                responses.extend(connect_API(url, params, None, int(responses[-1].get("tid"))))
                done = int(50 * (int(responses[-1].get("tid")) + 1) / total)
                sys.stdout.write('\r[{}{}]\t{}%'.format('█' * done, '.' * (50 - done), done * 2))
                sys.stdout.flush()
            except:
                print('KICKED OUT! RECONECTING...')
                responses = pd.DataFrame(responses)
                save_data(responses)
                responses = load_data()
                update(responses)
        sys.stdout.write('\n')
        print("\nDownload completed!")
        responses = pd.DataFrame(responses)
    save_data(responses)
    return responses


def update(responses):
    last_tid = responses.tail(1)["tid"].values[0]
    download_data(last_tid, responses)
    responses = load_data()
    return responses


def save_data(data):
    data.to_json(r'responses.json', orient='records')


def load_data():
    responses = pd.read_json(r'responses.json', orient='records')
    return responses


def difference(data):
    diff = np.zeros_like(data)
    for i in range(1, len(data)):
        diff[i] = data[i] - data[i - 1]
    return diff


def derivative(X, Y):
    div = np.zeros_like(Y)
    for i in range(len(Y) - 1):
        try:
            div[i] = (Y[i + 1] - Y[i]) / (int(X[i + 1]) / int(X[i]))
        except ZeroDivisionError:
            div[i] = 0
    return div


def LocMinMax(derivative, X, Y):
    Yminmax = []
    Xminmax = []
    for i in range(len(derivative) - 1):
        if derivative[i] * derivative[i + 1] <= 0:
            Xminmax.append(X[i])
            Yminmax.append(Y[i])
    return Xminmax, Yminmax


def main():
    pd.plotting.register_matplotlib_converters()
    if not path.exists('responses.json'):
        download_data()
        responses = load_data()
    else:
        responses = load_data()
        responses = update(responses)
    # print(responses)
    start = datetime.strptime(input("Podaj datę rozpoczęcia obserwacji (YYYY-MM-DD) (od 2014r): "), '%Y-%m-%d')
    end = datetime.strptime(input("Podaj datę zakończenia obserwacji (YYYY-MM-DD) (do dzisiaj): "), '%Y-%m-%d')
    # start = datetime.strptime('2020-04-01', '%Y-%m-%d')
    # end = datetime.strptime('2020-04-19', '%Y-%m-%d')

    SellTrades = responses[responses['type'] == 'sell']
    SellTrades = SellTrades[SellTrades['date'] >= start]
    SellTrades = SellTrades[SellTrades['date'] <= end]
    BuyTrades = responses[responses['type'] == 'buy']
    BuyTrades = BuyTrades[BuyTrades['date'] >= start]
    BuyTrades = BuyTrades[BuyTrades['date'] <= end]
    attribute_x = 'date'
    attribute_y = 'price'
    XBuy = BuyTrades[attribute_x].values
    YBuy = BuyTrades[attribute_y].values
    BuyDiff = difference(YBuy)
    BuyDiv = derivative(XBuy, YBuy)
    XBMinMax, YBMinMax = LocMinMax(BuyDiv, XBuy, YBuy)
    XSell = SellTrades[attribute_x].values
    YSell = SellTrades[attribute_y].values
    SellDiff = difference(YSell)
    SellDiv = derivative(XSell, YSell)
    XSMinMax, YSMinMax = LocMinMax(SellDiv, XSell, YSell)
    fig, ax = plt.subplots(1, 2, figsize=(30, 10))
    ax[0].plot(XBuy, YBuy, label='Price')
    ax[0].plot(XBuy, BuyDiff, label='Difference')
    ax[0].plot(XBuy, BuyDiv, label='Derivative')
    ax[0].plot(XBMinMax, YBMinMax, 'x', label='Maxima and minima')
    ax[0].set_title("Buy offerts BTC-USD")
    ax[0].set_xlabel("Date")
    ax[0].set_ylabel("Price [USD]")
    ax[1].plot(XSell, YSell, label='Price')
    ax[1].plot(XSell, SellDiff, label='Difference')
    ax[1].plot(XSell, SellDiv, label='Derivative')
    ax[1].plot(XSMinMax, YSMinMax, 'x', label='Maxima and minima')
    ax[1].set_title("Sell offerts BTC-USD")
    ax[1].set_xlabel("Date")
    ax[1].set_ylabel("Price [USD]")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
