import requests 
import numpy
import xlwt

def BTC_stats():

    response1 = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/")

    return response1.json()

def ETH_stats():

    response2 = requests.get("https://www.bitstamp.net/api/v2/ticker/ethusd/")

    return response2.json()

def LTC_stats():

    response3 = requests.get("https://www.bitstamp.net/api/v2/ticker/ltcusd/")

    return response3.json()

def BCH_stats():

    response4 = requests.get("https://www.bitstamp.net/api/v2/ticker/bchusd/")

    return response4.json()

def XRP_stats():

    response5 = requests.get("https://www.bitstamp.net/api/v2/ticker/xrpusd/")

    return response5.json()


def zasoby():

    tab = []
    price = []
    name = ["BTC","ETH","LTC","BCH","XRP"]

    print("Ile posiadasz BTC")
    tab.append(float(input()))
    if tab[0]==0:
        price.append(float(0))
    else:
        print("W jakiej cenie kupiłes BTC")
        price.append(float(input()))


    print("Ile posiadasz ETH")
    tab.append(float(input()))
    if tab[1]==0:
        price.append(float(0))
    else:
        print("W jakiej cenie kupiłes ETH")
        price.append(float(input()))


    print("Ile posiadasz LTC")
    tab.append(float(input()))
    if tab[2]==0:
        price.append(float(0))
    else:
        print("W jakiej cenie kupiłes LTC")
        price.append(float(input()))


    print("Ile posiadasz BCH")
    tab.append(float(input()))
    if tab[3]==0:
        price.append(float(0))
    else:
        print("W jakiej cenie kupiłes BCH")
        price.append(float(input()))

    print("Ile posiadasz XRP")
    tab.append(float(input()))
    if tab[4]==0:
        price.append(float(0))
    else:
        print("W jakiej cenie kupiłes XRP")
        price.append(float(input()))

    print("\n")
    print("Posiadane zasoby:")
    for i in range(5):
        print(tab[i],name[i],"kupione po cenie",price[i],"USD")


    BTC = BTC_stats()
    high_BTC = float(BTC["high"])
    low_BTC = float(BTC["low"])
    final_BTC = ((high_BTC/low_BTC)-1)*100
    bid_BTC = float(BTC["bid"])


    ETH = ETH_stats()
    high_ETH = float(ETH["high"])
    low_ETH = float(ETH["low"])
    final_ETH = ((high_ETH/low_ETH)-1)*100
    bid_ETH = float(ETH["bid"])


    LTC = LTC_stats()
    high_LTC = float(LTC["high"])
    low_LTC = float(LTC["low"])
    final_LTC = ((high_LTC/low_LTC)-1)*100
    bid_LTC = float(LTC["bid"])



    BCH = BCH_stats()
    high_BCH = float(BCH["high"])
    low_BCH = float(BCH["low"])
    final_BCH = ((high_BCH/low_BCH)-1)*100
    bid_BCH = float(BCH["bid"])



    XRP = XRP_stats()
    high_XRP = float(XRP["high"])
    low_XRP = float(XRP["low"])
    final_XRP = ((high_XRP/low_XRP)-1)*100
    bid_XRP = float(XRP["bid"])


    A = tab[0]*price[0] + tab[1]*price[1] + tab[2]*price[2] + tab[3]*price[3] + tab[4]*price[4]
    B = tab[0]*bid_BTC + tab[1]*bid_ETH + tab[2]*bid_LTC + tab[3]*bid_BCH + tab[4]*bid_XRP
    C = ((B/A)-1)*100
    if B > A:
        print("Po wykonaniu operacji wzrost ilości USD o",C,"%")
    elif A >B:
        print("Po wykonaniu operacji spadek ilości USD o",C,"%")
    elif A == B:
        print("Po wykonaniu operacji brak zmian w ilości USD")

    print("\n")
    print("Potencjalny zmiana na każdej z walut:")
    print("BTC",final_BTC,"%") 
    print("Na 1.0 BTC zmiana o",bid_BTC-price[0],"USD")
    print("ETH",final_ETH,"%")
    print("Na 1.0 ETH zmiana o",bid_ETH-price[1],"USD")
    print("LTC",final_LTC,"%")
    print("Na 1.0 LTC zmiana o",bid_LTC-price[2],"USD")
    print("BCH",final_BCH,"%")
    print("Na 1.0 BCH zmiana o",bid_BCH-price[3],"USD")
    print("XRP",final_XRP,"%")
    print("Na 1.0 XRP zmiana o",bid_XRP-price[4],"USD")
    
    wallet = xlwt.Workbook(encoding="utf-8")
    sheet1 = wallet.add_sheet("Wallet")
    sheet1.write(1, 1, "Posiadane zasoby")
    sheet1.write(1, 2, "Ilość")
    sheet1.write(1, 3, "Kupione po cenie")
    
    sheet1.write(2, 1, "BTC")
    sheet1.write(2, 2, tab[0])
    sheet1.write(2, 3, price[0])
    
    sheet1.write(3, 1, "ETH")
    sheet1.write(3, 2, tab[1])
    sheet1.write(3, 3, price[1])

    sheet1.write(4, 1, "LTC")
    sheet1.write(4, 2, tab[2])
    sheet1.write(4, 3, price[2])
    
    sheet1.write(5, 1, "BCH")
    sheet1.write(5, 2, tab[3])
    sheet1.write(5, 3, price[3])
    
    sheet1.write(6, 1, "XRP")
    sheet1.write(6, 2, tab[4])
    sheet1.write(6, 3, price[4])
    
    sheet1.write(7, 1, "Zmiana ilości USD po wykonaniu operacji w %")
    sheet1.write(7, 2, C)
    
    wallet.save("wallet.xls")
    return tab, name, price

tab, name, price=zasoby()