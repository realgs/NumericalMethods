import requests as rq
import json

def value_count2(base_currency, currency):
        obj = rq.get("https://bitbay.net/API/Public/"+currency+base_currency+"/trades.json?sort=desc").json()
        if obj == []:
                return(obj)
        else:
                return(obj[0]['price'])

def value_count(base_currency, currency, resources):
        obj = rq.get("https://bitbay.net/API/Public/"+currency+base_currency+"/orderbook.json?sort=desc").json()
        if obj == []:
                return(obj)
        else:
                amount = float(resources[currency])
                i = 0
                price = 0
                while (amount - obj['bids'][i][1]) >= 0:
                        amount = amount - obj['bids'][i][1]
                        price = price + (float(obj['bids'][i][1]) * float(obj['bids'][i][0]))
                        i += 1     
                price = price + float(obj['bids'][i][0]) * amount
        return price

def add(base_currency):
        while(input("Wciśnij ENTER aby dodać nową kryptowalute, wpisz END aby zakończyć dodawanie:") != "END"):
                currency  = input("Podaj kryptowalute(skrot np.:BTC,LTC):")
                if rate_update(base_currency, currency) == []:
                        print("Brak podanej kryptowaluty w API")
                else:
                        amount = input("Podaj ilosc posaidanej kryptowaluty:")
                        resources[currency] = amount

def edit(resources):
        while(input("Wciśnij ENTER aby edytowac kryptowalute, wpisz END aby zakończyć edycje:") != "END"):
                currency = input("Ktora walute chcesz edytowac?")
                if currency in resources.keys():
                        resources[currency] = input("Nowa ilosc danej waluty:")
                else:
                        print("Nie posiadasz takiej waluty")
        
def delete(resources):
        while(input("Wciśnij ENTER aby usunac kryptowalute, wpisz END aby zakończyć usuwanie z portfela:") != "END"):
                currency = input("Ktora walute chcesz usunac?")
                if currency in resources.keys():
                        del resources[currency]
                else:
                        print("Nie posiadasz takiej waluty")

def print_wallet(resources):
        print("Twoje aktualne zasoby i ich wartosc:")
        for currency in resources.keys():
                print(resources[currency], currency + " = cena z ofert skupu:", float(resources[currency]) * float(value_count(base_currency, currency, resources)), base_currency,", cena z ostatniej tranzakcji:",float(value_count2(base_currency, currency)) * float(resources[currency]))

resources = {}

with open('wallet.json', 'r') as openfile: 
    resources = json.load(openfile) 

base_currency = input("Podaj walute bazowa [PLN, EUR, USD, GBP]:")
while base_currency not in ['PLN', 'EUR', 'USD', 'GBP']:
        print("Podana waluta nie może być waluta bazowa, podaj inna walute z podanego przedzialu")
        base_currency = input("[PLN, EUR, USD, GBP]:")

i = input("Co chcesz zrobic? [a - dodanie nowej waluty, e - edycja juz istniejacej waluty, d - usuwanie waluty, pw - pokaz portfel,  END - pokaz portfel i zakoncz]:")
while i != "END":
        if i == 'a':
                add(base_currency)
        elif i == 'e':
                edit(resources)
        elif i == 'd':
                delete(resources)
        elif i == 'pw':
                print_wallet(resources)
        else:
                break
        i = input("Co chcesz zrobic? [a - dodanie nowej waluty, e - edycja juz istniejacej waluty, d - usuwanie waluty, pw - pokaz portfel,  END - pokaz portfel i zakoncz]:")

print_wallet(resources)

with open("wallet.json", "w") as outfile: 
    json.dump(resources, outfile) 