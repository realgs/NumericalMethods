import requests
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def get_50_transactions(id):
    url = "https://bitbay.net/API/Public/BTCUSD/trades.json?since=" + str(id)
    response = requests.get(url).json()
    transactions = pd.DataFrame(response)
    return transactions


def complete_data():
    start_id = 292759   #id of first operation in 2020. Set on this level to shorten download time.
    print('\nPobieram dane ... (ok. 2 minuty)')
    first_data_part = get_50_transactions(id=start_id)
    last_id = first_data_part['tid'].iloc[-1]

    while get_50_transactions(last_id).shape[0] == 50:
        data_part = get_50_transactions(id=last_id)
        first_data_part = first_data_part.append(data_part, ignore_index=True)
        last_id = first_data_part['tid'].iloc[-1]

    last_data_part = get_50_transactions(id=last_id)
    data = first_data_part.append(last_data_part, ignore_index=True)
    data = data.drop(columns=['amount', 'type', 'tid'])
    data['date'] = pd.to_datetime(data['date'], unit='s')
    print('\nPobieranie zakończone.')

    return data


def prepare_data():
    data = complete_data()
    val_data = data.loc[(data['date'] < end + datetime.timedelta(days=8)) & (data['date'] > end)]
    train_data = data.loc[(data['date'] >= start) & (data['date'] <= end + datetime.timedelta(days=1))]
    val_data = val_data.groupby([pd.Grouper(key='date', freq='D')]).mean().reset_index()
    columns = train_data.columns.difference(['date'])
    train_data[columns].astype(float)
    train_data = train_data.resample('d', on='date').mean().dropna(how='all')
    change = train_data['price'].pct_change().fillna(0)
    train_data = train_data.assign(change=change.values)
    train_data = train_data.reset_index()
    train_data['day of week'] = train_data['date'].dt.day_name()

    return train_data, val_data


def day_probability(day_name, data):
    daily_data = data.loc[data['day of week'] == day_name]
    day_changes = daily_data['change'].to_numpy()
    decreases_amount = np.sum(day_changes < 0)
    increases_amount = np.sum(day_changes > 0)
    all_changes = data['change'].to_numpy()
    increases = all_changes[all_changes > 0]
    decreases = all_changes[all_changes < 0]

    if decreases_amount > increases_amount:
        pick = np.random.choice(decreases)
    elif increases_amount > decreases_amount:
        pick = np.random.choice(increases)
    else:
        pick = np.random.choice(all_changes)

    return pick


def generate_dates():
    dates_to_predict = []
    days_to_predict = []

    for i in range(1, 8):
        date = end + datetime.timedelta(days=i)
        day = date.strftime('%A')
        dates_to_predict.append(date)
        days_to_predict.append(day)

    return dates_to_predict, days_to_predict


def prediction(data):
    days = generate_dates()[1]
    changes = []
    for day in days:
        changes.append(day_probability(day, data))

    last_price = data.iloc[-1]['price']
    predicted_prices = [0] * len(changes)
    for i in range(len(changes)):
        predicted_prices[i] = last_price + changes[i]*last_price
        last_price = predicted_prices[i]

    predicted_prices.insert(0, data.iloc[-1]['price'])
    predicted_dates = generate_dates()[0]
    predicted_dates.insert(0, data.iloc[-1]['date'])

    return predicted_dates, predicted_prices


def user_start_input():
    while True:
        try:
            inp = input("Podaj datę początkową badania yyyy-mm-dd (tylko 2020 r. i więcej niż 3tygodnie wstecz): ")
            start = datetime.datetime.strptime(inp, "%Y-%m-%d")
            while start < datetime.datetime.strptime('2020-01-01', '%Y-%m-%d') or start > datetime.datetime.today() - datetime.timedelta(days=21):
                print('Wprowadziłeś datę spoza zakresu!')
                while True:
                    try:
                        inp = input("Podaj datę początkową badania yyyy-mm-dd (tylko 2020 r. i więcej niż 3 tygodnie wstecz): ")
                        start = datetime.datetime.strptime(inp, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Wprowadziłeś zły format!")
            break
        except ValueError:
            print("Wprowadziłeś zły format!")

    return start


def user_end_input():
    while True:
        try:
            inp = input("Podaj datę końcową badania yyyy-mm-dd (tylko 2020 r. więcej niż tydzień wstecz i zalecana min 2tyg po początkowej): ")
            end = datetime.datetime.strptime(inp, "%Y-%m-%d")
            while end < start + datetime.timedelta(days=14) or end > datetime.datetime.today() - datetime.timedelta(days=7):
                print('Wprowadziłeś datę spoza zakresu!')
                while True:
                    try:
                        inp = input("Podaj datę początkową badania yyyy-mm-dd (tylko 2020 r. i zalecana min 2tyg po początkowej): ")
                        end = datetime.datetime.strptime(inp, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Wprowadziłeś zły format!")
            break
        except ValueError:
            print("Wprowadziłeś zły format!")

    return end


def main():
    data, val_data = prepare_data()
    print('\nTworzę wykres...')

    errors = {}
    predictions = []
    for i in range(100):
        dates, prices = prediction(data)
        predictions.append(prices)
        mse = 0
        for k in range(len(prices)):
            mse += ((prices[k] - val_data['price'][k])**2)/len(prices)
        errors.update({mse: prices})
        plt.plot(dates, prices, 'lightskyblue')

    lowest_mse = min([float(i) for i in errors])
    predictions_arr = np.array(predictions)
    average_prediction = np.mean(predictions_arr, axis=0)
    whole_data = data.append(val_data, ignore_index=True, sort=True)

    plt.plot(whole_data['date'], whole_data['price'], 'blue', label='Real Bitcoin exchange rate')
    plt.plot(prediction(data)[0], average_prediction, 'black', label='Average of 100 simulations')
    plt.plot(prediction(data)[0], errors[lowest_mse], 'red', label='Simulation with lowest MeanSquareError')

    if data['date'].shape[0] > 21:
        decision = (input('\nChcesz obejrzeć tylko fragment wykresu, aby lepiej widzieć predykcję? (tak/nie): '))
        if decision.upper() == 'TAK':
            plt.xlim([end - datetime.timedelta(days=14), end + datetime.timedelta(days=7)])
        else:
            plt.xlim(start, end + datetime.timedelta(days=7))
    else:
        plt.xlim(start, end + datetime.timedelta(days=7))

    plt.xlabel('Date')
    plt.ylabel('Price [USD]')
    plt.title('BTC price with 7-days prediction')
    plt.legend()
    fig = plt.gcf()
    fig.set_size_inches(36, 14)
    plt.show()

    print('\nStatystyki symulacji:')
    print('Średnia: ', np.mean(average_prediction))
    print('Mediana:', np.median(average_prediction))
    print('Odchylenie standardowe:', np.std(average_prediction))
    print('Najmniejszy błąd średniokwadratowy (zielony wykres): ', lowest_mse)


start = user_start_input()
end = user_end_input()
main()
