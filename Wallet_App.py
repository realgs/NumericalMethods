import tkinter as tk
import requests
import json
from tkinter import messagebox
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


def get_bitstamp_24h(type):
    request = requests.get("https://www.bitstamp.net/api/v2/ticker/{}usd/".format(type))
    return request.json()


def get_bitstamp_orderbook(type):
    request = requests.get("https://www.bitstamp.net/api/v2/transactions/{}usd/".format(type))
    return request.json()


def plot():
    global label

    try:
        key = entry_type.get()
        info = get_bitstamp_orderbook(key)
        new_window = tk.Toplevel(root)
        list_buy = []

        for i in range(len(info)):
            if info[i]['type'] == '0':
                list_buy.append(float(info[i]['price']))

        figure = Figure(figsize=(5, 4), dpi=100)
        plot_prices = figure.add_subplot(1, 1, 1)
        plot_prices.plot(list_buy)
        plot_label = tk.Label(new_window, text="Buy price change over the last 24 hours")
        plot_label.pack()
        canvas = FigureCanvasTkAgg(figure, new_window)
        canvas.get_tk_widget().pack()
        label['text'] = "Showing graph"

    except:

        label['text'] = "Please put specified crypto currency type in bracket "


def add_to_wallet():
    global my_wallet
    global label

    crypto_list = ['btc', 'eth','ltc','xrp']
    try:
        if entry_type.get() in crypto_list:

            list_of_keys = []
            for keys, items in my_wallet.items():
                list_of_keys.append(keys)

            if entry_type.get() in list_of_keys:
                wallet_data = my_wallet[entry_type.get()]
                wallet_data = float(wallet_data)
                to_add = float(entry_amount.get()) + wallet_data
                to_add = str(to_add)
                my_wallet.update({entry_type.get(): to_add})
                label['text'] = "added {} more {} to wallet".format(entry_amount.get(), entry_type.get())

            else:
                my_wallet[entry_type.get()] = entry_amount.get()
                position = len(my_wallet)
                label['text'] = "added to wallet\n\ncurrent number of positions in wallet {}.".format(position)
        else:
            label['text'] = "Please input amount and correct crypto currency type"
    except:
        label['text'] = "Please input amount and crypto currency type"


def reset_wallet():
    global my_wallet
    global label

    question = messagebox.askyesno("Notice", "Are you sure you want to reset your wallet?",
                                   icon='warning')

    if question:
        my_wallet = {}
        label['text'] = "Wallet reset"
    else:
        pass


def save_wallet():
    global my_wallet
    global label

    question = messagebox.askyesno("Notice", "Are you sure you want to save ?\nSaving will overwrite the data",
                                   icon='warning')

    if question:
        with open("wallet_file.json", "w") as json_file:
            json.dump(my_wallet, json_file)
        label['text'] = "Wallet saved"

    else:
        pass


def upload_wallet():
    global my_wallet

    with open('wallet_file.json') as json_file:
        data = json.load(json_file)

    my_wallet = data

    label['text'] = "Wallet loaded"


def compare():
    global my_wallet
    global label

    new_window = tk.Toplevel(root)

    my_label = tk.Label(new_window, text="Comparing current price with price from 24 hours ago\n\n")
    my_label.pack()

    for key, items in my_wallet.items():

        try:
            wallet_value = my_wallet[key]

        except:
            label['text'] = "you didn't add any values or named the values wrong" \
                            "\n please name them acordingly (bitcoin = btc, Etherum = eth etc.)"
            pass

        try:
            info = get_bitstamp_24h(key)

        except:
            label['text'] = "Error: bitstamp API doesn't support your cryptocurrency or please name it accordingly" \
                            "\n(bitcoin = btc, Ethereum = eth etc.)"
            pass

        first_price = info['open']
        current_price = info['last']

        wallet_value = float(wallet_value)
        first_price = float(first_price)
        current_price = float(current_price)

        first_price = wallet_value * first_price
        current_price = wallet_value * current_price

        comparison = ((current_price - first_price) / current_price) * 100

        for_label = str(comparison)

        my_label = tk.Label(new_window, text="\n{} Ratio: {} %".format(key, for_label))
        my_label.pack()


def wallet_value():
    global my_wallet
    global label

    wallet_sum = 0
    compare_value = 0

    for key, item in my_wallet.items():

        try:
            wallet_value = my_wallet[key]

        except:

            label['text'] = "you didn't add any values or named the values wrong" \
                            "\n please name them acordingly (bitcoin = btc, Etherum = eth etc.)"
            pass

        try:
            info = get_bitstamp_24h(key)

        except:
            label['text'] = "Error: bitstamp API doesn't support your cryptocurrency or please name it accordingly\n" \
                            "(bitcoin = btc, Etherum = eth etc.)"

        wallet_value = float(wallet_value)
        first_price = info['open']
        first_price = float(first_price)
        current_price = info['last']
        current_price = float(current_price)

        to_add = wallet_value * current_price

        wallet_sum = wallet_sum + to_add

        difference = (wallet_value * current_price) - (wallet_value * first_price)
        compare_value = difference + compare_value

    wallet = ','.join("{}: {}".format(k, v) for k, v in my_wallet.items())
    compare_value = round(compare_value, 3)

    label['text'] = "your current wallet value: {} USD\n\nDiffrence in value based on your wallet and prices from 24h " \
                    "is: {} USD\n your wallet:\n {}".format(wallet_sum, compare_value, wallet)


def Change_wallet():
    global my_wallet
    global label
    list_of_keys = []

    for key, items in my_wallet.items():
        list_of_keys.append(key)

    if entry_type.get() in list_of_keys:
        my_wallet.update({entry_type.get(): entry_amount.get()})
        label['text'] = "Wallet changed"

    elif entry_type.get() not in list_of_keys:
        label['text'] = "First add an item to wallet to change it"

    else:
        label['text'] = "Such crypto currency isn't supported"

# main
my_wallet = {}

root = tk.Tk()

root.title("Wallet")


entry_amount_label = tk.Label(root, text="Enter your crypto currency amount")
entry_amount_label.pack()

entry_amount = tk.Entry(root, width=50)
entry_amount.pack()

entry_type_label = tk.Label(root, text='Specify crypto currency (btc,ltc,eth,xrp)')
entry_type_label.pack()

entry_type = tk.Entry(root, width=50)
entry_type.pack()

# buttons

# adds to wallet
button1 = tk.Button(root, text='add to wallet', command=add_to_wallet, pady=5, padx=5)
button1.pack(fill='x')

# Change wallet
button7 = tk.Button(root, text="Change value in your wallet", command=Change_wallet, padx=5, pady=5)
button7.pack(fill='x')

# add existing wallet button

button4 = tk.Button(root, text="Upload last wallet", command=upload_wallet, padx=5, pady=5)
button4.pack(fill='x')

# show wallet value button

button5 = tk.Button(root, text="Wallet value in USD", command=wallet_value, padx=5, pady=5)
button5.pack(fill='x')

# compares with 24h price button in %
button5 = tk.Button(root, text="Compare prices", command=compare, padx=5, pady=5)
button5.pack(fill='x')

# saves wallet to json button

button3 = tk.Button(root, text="Save your wallet \n Warning!: saving will override existing data", command=save_wallet)
button3.pack(fill='x')

# reset wallet button

button6 = tk.Button(root, text="Reset wallet", command=reset_wallet, padx=5, pady=5)
button6.pack(fill='x')

#
button8 = tk.Button(root, text="Show price change graph", command=plot, padx=5, pady=5)
button8.pack(fill='x')
# exits program

exit_button = tk.Button(root, text="Exit Program", command=root.quit, padx=5, pady=5)
exit_button.pack(fill='x')

# Notice

notice_bar = tk.Label(root, text="Notice:")
notice_bar.pack()

# Label
label = tk.Label(root, text="hello")
label.pack()

root.mainloop()
