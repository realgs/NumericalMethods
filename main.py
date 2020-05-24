import pandas as pd
import matplotlib.pyplot as plt
import prediction_from_probability as pfp
import numpy as np

# import RecurrentNeuralNetwork as RNN
# import datetime
# import os
# from keras.models import load_model


# def rnn_model(date):
#     df = pfp.download_data('2011-01-01', peroid='1DAY')
#     df = df[['price_close', 'time_close']]
#     df['time_close'] = df['time_close'].dt.date
#     df = df.groupby('time_close').mean()['price_close']
#     year, month, day = date.split('-')
#     year = int(year)
#     month = int(month)
#     day = int(day)
#     time = (datetime.datetime.today() - datetime.datetime(year, month, day)).days + 1
#     if os.path.exists('btc_prediction_model.h5'):
#         model = load_model('btc_prediction_model.h5')
#     else:
#         price_matrix = RNN.price_martix(df, length=time)
#         price_matrix = RNN.normalize_data(price_matrix)
#         row, X_train, Y_train, X_test, Y_test = RNN.split(price_matrix)
#         model = RNN.set_model(time, X_train, Y_train)
#     pretict_data = RNN.create_df(X_train.index[-1], time)
#     price = RNN.price_martix(pretict_data, time)
#     X_test = RNN.normalize_data(price)
#     X_test = np.array(X_test)
#     X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
#     preds = model.predict(X_test,batch_size=3)
#     return preds


if __name__ == '__main__':
    date = input("Podaj date w formacie YYYY-MM-DD (mogą być od 2011 - ale liczenie zajmie wieki - najlepiej wziąć od początku roku): ")
    # date = '2020-05-01'
    while not pfp.check_date(date):
        print('Wprowadzono nieprawidłową datę!')
        print('Aby wyjść z programu wpisz q')
        date = input("Podaj date w formacie YYYY-MM-DD: ")
        if date == 'q':
            exit()

    df = pfp.download_data(date, peroid='1HRS')
    df, prediction_data = pfp.extend_df(df, date, peroid='1HRS')
    predictionmean = pd.DataFrame(columns=['price_close', 'time_close'])
    print("Symulacja...")
    for i in range(0,100,10):
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