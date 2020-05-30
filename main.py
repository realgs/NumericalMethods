import pandas as pd
import matplotlib.pyplot as plt
import prediction_from_probability as pfp
import numpy as np

if __name__ == '__main__':
    date = '2019-05-01'
    end = '2020-02-01'

    df = pfp.download_data(date, peroid='1HRS')
    df, prediction_data = pfp.extend_df(df, date, peroid='1HRS')
    predictionmean = pd.DataFrame(columns=['price_close', 'time_close'])
    print("Symulacja...")
    for i in range(0, 100, 10):
        pos, a, delta = pfp.create_matrix(df)
        print('{}%'.format(i))
        delta = pfp.change_matrix(pos / a, i / 100, delta)
        predictionmean = predictionmean.append(
            pfp.predict(delta, prediction_data, df.iloc[-1], i / 100, int(np.ceil(len(prediction_data.index) / 8)), df)[
                ['price_close', 'time_close']])
    predictionmean = predictionmean.groupby('time_close').mean()
    pos, a, delta = pfp.create_matrix(df)
    delta = pfp.change_matrix(pos / a, 0.6, delta)
    print("Tworzenie najlepszego modelu...")
    prediction_data = pfp.predict(delta, prediction_data, df.iloc[-1], 0.6, 7, df)

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

    print("Statystyki dla 100-krotnej symulacji: ")
    print("Średnia: {}".format(np.mean(predictionmean['price_close'])))
    print("Mediana: {}".format(np.median(predictionmean['price_close'])))
    print("Odchylenie standardowe: {}".format(np.std(predictionmean['price_close'])))
    print("Statystyki dla pojedynczej symulacji: ")
    print("Średnia: {}".format(np.mean(prediction_data['price_close'])))
    print("Mediana: {}".format(np.median(prediction_data['price_close'])))
    print("Odchylenie standardowe: {}".format(np.std(prediction_data['price_close'])))
