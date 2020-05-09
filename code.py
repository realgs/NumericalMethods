import requests
import csv
import os


def get_tickers_in_USD():
    BTC = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/")
    EUR = requests.get("https://www.bitstamp.net/api/v2/ticker/eurusd/")
    XRP = requests.get("https://www.bitstamp.net/api/v2/ticker/xrpusd/")
    LTC = requests.get("https://www.bitstamp.net/api/v2/ticker/ltcusd/")
    ETH = requests.get("https://www.bitstamp.net/api/v2/ticker/ethusd/")
    BCH = requests.get("https://www.bitstamp.net/api/v2/ticker/bchusd/")

    return BTC.json(), EUR.json(), XRP.json(), LTC.json(), ETH.json(), BCH.json()


def get_tickers_in_EUR():
    BTC = requests.get("https://www.bitstamp.net/api/v2/ticker/btceur/")
    XRP = requests.get("https://www.bitstamp.net/api/v2/ticker/xrpeur/")
    LTC = requests.get("https://www.bitstamp.net/api/v2/ticker/ltceur/")
    ETH = requests.get("https://www.bitstamp.net/api/v2/ticker/etheur/")
    BCH = requests.get("https://www.bitstamp.net/api/v2/ticker/bcheur/")

    return BTC.json(), XRP.json(), LTC.json(), ETH.json(), BCH.json()


def input_your_cryptos():
    resources = {}
    BTC, EUR, XRP, LTC, ETH, BCH = get_tickers_in_USD()
    list_of_cryptos = [BTC, EUR, XRP, LTC, ETH, BCH]
    list_of_names = ['BTC', 'EUR', 'XRP', 'LTC', 'ETH', 'BCH']
    print("You can choose a resource from {}\n"
          "Q to quit".format(list_of_names))
    with open('resources.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        while True:
            name = input("Enter the name of the resource: ").upper()
            if name == 'Q':
                return resources
            elif name in list_of_names:
                index = list_of_names.index(name)
                if list_of_cryptos[index]['volume'] == 0:
                    print("{} isn't available right now".format(name))
                    continue
                else:
                    quantity = float(input("Enter the quantity of the resource: "))

                    formula = round(((float(list_of_cryptos[index]['last']) - float(
                        list_of_cryptos[index]['vwap'])) / float(list_of_cryptos[index]['last'])) * 100, 2)

                    resources[name] = quantity
                    csv_writer.writerow([name, quantity, formula])
            else:
                print("Wrong input")


def resource_check():
    print("Your resources are:\n"
          "Name and quantity")
    with open('resources.csv', 'r') as readFile:
        reader = csv.reader(readFile, delimiter=',')
        for row in reader:
            print(row[0], row[1])


def percentage_check():
    with open('resources.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        perecentage_sum = 0
        for row in csv_reader:
            if float(row[2]) > 0:
                print("{} is now +{}%".format(row[0], round(float(row[2]), 3)))
            elif float(row[2]) == 0:
                print("0%")
            else:
                print("{} is now {}%".format(row[0], round(float(row[2]), 3)))
            perecentage_sum += float(row[2])
        print("You've gained/lost {}%".format(round(perecentage_sum, 3)))


def value_check_USD():
    BTC, EUR, XRP, LTC, ETH, BCH = get_tickers_in_USD()
    list_of_cryptos = [BTC, EUR, XRP, LTC, ETH, BCH]
    list_of_names = ['BTC', 'EUR', 'XRP', 'LTC', 'ETH', 'BCH']
    with open('resources.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            name = row[0]
            index = list_of_names.index(name)
            price = float(list_of_cryptos[index]['vwap'])
            amount = float(row[1])
            print("Your {} costs now {} USD".format(name, round(price * amount, 2)))


def value_check_EUR():
    BTC, XRP, LTC, ETH, BCH = get_tickers_in_EUR()
    list_of_cryptos = [BTC, XRP, LTC, ETH, BCH]
    list_of_names = ['BTC', 'XRP', 'LTC', 'ETH', 'BCH']
    with open('resources.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            name = row[0]
            if name == 'EUR':
                print("Your EUR is still {}".format(row[1]))
            else:
                index = list_of_names.index(name)
                price = float(list_of_cryptos[index]['vwap'])
                amount = float(row[1])
                print("Your {} costs now {} EUR".format(name, round(price * amount, 2)))


def adding_resource():
    resources = {}
    BTC, EUR, XRP, LTC, ETH, BCH = get_tickers_in_USD()
    list_of_cryptos = [BTC, EUR, XRP, LTC, ETH, BCH]
    list_of_names = ['BTC', 'EUR', 'XRP', 'LTC', 'ETH', 'BCH']
    print("Your resources are: ")
    with open('resources.csv', 'r') as readFile:
        reader = csv.reader(readFile, delimiter=',')
        for row in reader:
            print(row[0], row[1])
    name = input("Enter the name of the resource \n"
                 "Q to quit: ").upper()
    if name in list_of_names:
        with open('resources.csv', 'a') as appendFile:
            writer = csv.writer(appendFile)
            index = list_of_names.index(name)
            if list_of_cryptos[index]['volume'] == 0:
                print("{} isn't available right now".format(name))
            else:
                quantity = float(input("Enter the quantity of the resource: "))
                formula = round(
                    ((float(list_of_cryptos[index]['last']) - float(list_of_cryptos[index]['vwap'])) / float(
                        list_of_cryptos[index]['last'])) * 100, 2)
                resources[name] = quantity
                writer.writerow([name, quantity, formula])
        print("{} appended".format(name))
    elif name == 'Q':
        print("Closed")
    else:
        print("Wrong input")


def deleting_resource():
    list_of_names = ['BTC', 'EUR', 'XRP', 'LTC', 'ETH', 'BCH']
    lines = list()
    print("Your resources are: ")
    with open('resources.csv', 'r') as readFile:
        reader = csv.reader(readFile, delimiter=',')
        for row in reader:
            print(row[0])
    name = input("Which resource would you like to delete? \n"
                 "Q to quit: ").upper()
    if name in list_of_names:
        with open('resources.csv', 'r') as readFile:
            reader = csv.reader(readFile, delimiter=',')
            for row in reader:
                lines.append(row)
                for element in row:
                    if element == name:
                        lines.remove(row)
        print("{} deleted".format(name))
        with open('resources.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
    elif name == 'Q':
        print("Closed")
    else:
        print("Wrong input")


def changing_quantity():
    lines = list()
    list_of_names = ['BTC', 'EUR', 'XRP', 'LTC', 'ETH', 'BCH']
    print("Your resources are: ")
    with open('resources.csv', 'r') as readFile:
        reader = csv.reader(readFile, delimiter=',')
        for row in reader:
            print(row[0], row[1])
    name = input("Which resource would you like to change? ").upper()
    if name in list_of_names:
        quantity = input("What's the new quantity? ")
        with open('resources.csv', 'r') as readFile:
            reader = csv.reader(readFile, delimiter=',')
            for row in reader:
                lines.append(row)
                for element in row:
                    if element == name:
                        row[1] = quantity
        with open('resources.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        print("{} quantity changed".format(name))
    elif name == 'Q':
        print("Closed")
    else:
        print("Wrong input")


def clear_resources():
    with open('resources.csv', 'w') as readFile:
        readFile.truncate()
    print("All resources deleted")


def check_if_empty():
    file_path = 'resources.csv'
    if os.stat(file_path).st_size == 0:
        return True
