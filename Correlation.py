from FinantialAPI_plot import download_data, load_data, update, save_data
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from os import path
import pandas as pd


def ArrayMaker(df, tradetype, start, end):
    arr = df[df['type'] == tradetype]
    arr = arr[arr['date'] >= start]
    arr = arr[arr['date'] <= end]
    # arr['date'] = pd.to_datetime(arr['date']).dt.date
    return arr.reset_index()


def main():
    pd.plotting.register_matplotlib_converters()
    if not path.exists('responses.json'):
        download_data()
        responses = load_data()
    else:
        responses = load_data()
        responses = update(responses)
    start = datetime.strptime('2020-05-01', '%Y-%m-%d')
    end = datetime.strptime('2020-05-02', '%Y-%m-%d')
    Sell = ArrayMaker(responses, 'sell', start, end)
    Buy = ArrayMaker(responses, 'buy', start, end)
    # Pearson correlation coefficient for Sells
    Xs = Sell['price'].values - Sell['price'].mean()
    Ys = Sell['amount'].values - Sell['amount'].mean()
    SellPearsonNumerator = Xs.T @ Ys
    SellPearsonDenominator = np.sqrt(Xs.T @ Xs) * np.sqrt(Ys.T @ Ys)
    SellPearson = SellPearsonNumerator / SellPearsonDenominator
    # Pearson correlation coefficient for Buys
    Xb = Buy['price'].values - Buy['price'].mean()
    Yb = Buy['amount'].values - Buy['amount'].mean()
    BuyPearsonNumerator = Xb.T @ Yb
    BuyPearsonDenominator = np.sqrt(Xb.T @ Xb) * np.sqrt(Yb.T @ Yb)
    BuyPearson = BuyPearsonNumerator / BuyPearsonDenominator
    fig, ax = plt.subplots(1, 2, figsize=(30, 10))
    ax[0].scatter(Sell['price'], Sell['amount'])
    ax[0].set_title("[Sell] Pearson correlation coefficient: {}".format(SellPearson))
    ax[0].set_xlabel("Price [USD]")
    ax[0].set_ylabel("Amount")
    ax[1].scatter(Buy['price'], Buy['amount'])
    ax[1].set_title("[Buy] Pearson correlation coefficient: {}".format(BuyPearson))
    ax[1].set_xlabel("Price [USD]")
    ax[1].set_ylabel("Amount")
    plt.show()
    return 0


if __name__ == "__main__":
    main()
