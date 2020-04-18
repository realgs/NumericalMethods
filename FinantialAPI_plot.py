from FinancialAPI import connect_API
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import json
from os import path
import pandas as pd


def download_data(upd_idx=None, responses=None):
    params = [['BTC', 'USD'], 'trades']
    url = "https://bitbay.net/API/Public/"
    if upd_idx:
        print("UPDATING DATABASE...")
        responses_n = connect_API(url, params, None, upd_idx)
        while len(responses_n) % 50 == 0 and len(responses_n) > 0:
            responses_n.extend(connect_API(url, params, None, int(responses_n[-1].get("tid"))))
        print("UPDATE COMPLETED (updated {} rows)".format(int(responses_n[-1].get("tid")) - upd_idx)) if len(
            responses_n) > 0 else print("Nothing to update!")
        responses_n = pd.DataFrame(responses_n)
        responses.append(responses_n, ignore_index=True)
        return responses
    # TODO saving update changes

    else:
        responses = connect_API(url, params)
        print("Downloading data...\nIt will take about 10-15 minutes!!")
        while len(responses) % 50 == 0:
            responses.extend(connect_API(url, params, None, int(responses[-1].get("tid"))))
        print("Download completed!")
    save_data(responses, upd_idx)
    return responses


def update(responses):
    last_tid = responses.tail(1)["tid"].values[0]
    print(last_tid)
    responses = download_data(last_tid, responses)
    return responses


def save_data(data, upd_idx):
    print(data)
    if upd_idx:
        data.to_json(r'responses.json')
    else:
        with open('responses.json', 'w') as json_file:
            json.dump(data, json_file)


def load_data():
    responses = pd.read_json(r'responses.json')
    return responses


def time_change(responses):
    for response in responses:
        response['date'] = datetime.utcfromtimestamp(response['date']).strftime('%Y-%m-%d %H:%M:%S')
    pass


def main():
    if not path.exists('responses.json'):
        responses = download_data()
    else:
        responses = load_data()
        responses = update(responses)
    # print(responses)
    # start = datetime.strptime(input("Podaj datę rozpoczęcia obserwacji (YYYY-MM-DD): "), '%Y-%m-%d')
    # end = datetime.strptime(input("Podaj datę zakończenia obserwacji (YYYY-MM-DD): "), '%Y-%m-%d')
    start = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end = datetime.strptime('2020-04-18', '%Y-%m-%d')

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
    XSell = SellTrades[attribute_x].values
    YSell = SellTrades[attribute_y].values
    fig, ax = plt.subplots(1, 2, figsize=(20, 10),dpi=300)
    ax[0].plot(XBuy, YBuy)
    ax[0].set_title("Buy")
    ax[0].set_xlabel("Date")
    ax[0].set_ylabel("Price")
    ax[1].plot(XSell, YSell)
    ax[1].set_title("Sell")
    ax[1].set_xlabel("Date")
    ax[1].set_ylabel("Price")
    # plt.ylim((0, 20000))
    plt.show()


if __name__ == '__main__':
    main()
