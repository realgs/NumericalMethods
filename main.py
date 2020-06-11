import pandas as pd
import matplotlib.pyplot as plt
import prediction_from_probability as pfp
import numpy as np
import datetime
import warnings

warnings.filterwarnings("ignore")

if __name__ == '__main__':
    date = '2019-05-01'
    end = '2020-03-01'

    df = pfp.download_data(date, end, peroid='1HRS')

    predictionmean = pd.DataFrame(columns=['price_close', 'time_close'])
    split_index = df.loc[df['time_open'] == datetime.datetime(2019, 10, 1)].index[0]
    learning_set = df.iloc[:split_index, :]
    learning_set['return'] = learning_set['price_close'] - learning_set['price_open']
    df2 = df.iloc[split_index:, :]
    df2 = df2.reset_index(drop=True)
    print("Symulacja...")
    for i in range(0, 50):
        pos, a, delta = pfp.create_matrix(learning_set)
        print('{}%'.format((i + 1) * 100 / 50))
        delta = pfp.change_matrix(pos / a, 0.6, delta)
        predictionmean = predictionmean.append(
            pfp.predict(delta, df2.copy(), learning_set.iloc[-1].copy(), 0.6, int(np.ceil(len(df2.index) / 30)),
                        learning_set.copy())[['price_close', 'time_close']])
    predictionmean = predictionmean.groupby('time_close').mean()

    pos, a, delta = pfp.create_matrix(learning_set)
    delta = pfp.change_matrix(pos / a, 0.6, delta)
    print("Tworzenie najlepszego modelu...")
    prediction_data = pfp.predict(delta, df2.copy(), learning_set.iloc[-1].copy(), 0.6, 7, learning_set.copy())

    plt.figure(figsize=(16, 9))
    plt.plot(prediction_data['time_close'], predictionmean['price_close'], color='blue', alpha=1,
             label='średnia z symulacji')
    plt.plot(prediction_data['time_close'], prediction_data['price_close'], color='orange',
             label='Pojedyncza predykcja')

    plt.plot(df['time_close'], df['price_close'], color='black', label='Pobrane dane')
    plt.title("Predykcja kursu BTC - USD")
    plt.xticks(rotation='vertical')
    plt.xlabel('Date')
    plt.ylabel('Price [USD]')
    plt.legend()
    plt.savefig('prediction.png')
    plt.show()
    rmse_sym = np.sqrt(np.mean(((predictionmean['price_close'].values - df2['price_close'].values) ** 2)))
    rmse_sin = np.sqrt(np.mean(((prediction_data['price_close'].values - df2['price_close'].values) ** 2)))
    print("Statystyki: ")
    print("Średni błąd kwadratowy dla pojedynczej sym: {}".format(rmse_sin))
    print("Średni błąd kwadratowy dla 100 sym: {}".format(rmse_sym))
