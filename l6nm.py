import requests
import numpy
import xlwt


def BTC_stats():
    response1 = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/")
    return response1.json()

def LTC_stats():
    response2 = requests.get("https://www.bitstamp.net/api/v2/ticker/ltcusd/")
    return response2.json()

def BCH_stats():
    response3 = requests.get("https://www.bitstamp.net/api/v2/ticker/bchusd/")
    return response3.json()

def XRP_stats():
    response4 = requests.get("https://www.bitstamp.net/api/v2/ticker/xrpusd/")
    return response4.json()

def ETH_stats():
    response5 = requests.get("https://www.bitstamp.net/api/v2/ticker/ethusd/")
    return response5.json()

names = ['BTC','LTC','BCH','XRP','ETH']

def crypto():
    amount_currency=[]
    value=[]
    amount_currency.append(float(input('Ile chcesz BTC: ')))
    if amount_currency[0]==0:
        value.append(float(0))
    else:
        value.append(float(input('Za ile kupiłeś BTC: ')))
    amount_currency.append(float(input('Ile chcesz LTC: ')))
    if amount_currency[1]==0:
        value.append(float(0))
    else:
        value.append(float(input('Za ile kupiłeś LTC: ')))
    amount_currency.append(float(input('Ile chcesz BCH: ')))
    if amount_currency[2]==0:
        value.append(float(0))
    else:
        value.append(float(input('Za ile kupiłeś BCH: ')))
    amount_currency.append(float(input('Ile chcesz XRP: ')))
    if amount_currency[3]==0:
        value.append(float(0))
    else:
        value.append(float(input('Za ile kupiłeś XRP: ')))
    amount_currency.append(float(input('Ile chcesz ETH: ')))
    if amount_currency[4]==0:
        value.append(float(0))
    else:
        value.append(float(input('Za ile kupiłeś ETH: ')))
   

    BTC = BTC_stats()
    h_BTC = float(BTC["high"])
    l_BTC = float(BTC["low"])
    f_BTC = ((h_BTC/l_BTC)-1)*100
    b_BTC = float(BTC["bid"])       
    p_BTC = b_BTC-value[0]
    
    LTC = LTC_stats()
    h_LTC = float(LTC["high"])
    l_LTC = float(LTC["low"])
    f_LTC = ((h_LTC/l_LTC)-1)*100
    b_LTC = float(LTC["bid"])
    p_LTC = b_LTC-value[1]
    
    BCH = BCH_stats()
    h_BCH = float(BCH["high"])
    l_BCH = float(BCH["low"])
    f_BCH = ((h_BCH/l_BCH)-1)*100
    b_BCH = float(BCH["bid"])
    p_BCH = b_BCH-value[2]
    
    XRP = XRP_stats()
    h_XRP = float(XRP["high"])
    l_XRP = float(XRP["low"])
    f_XRP = ((h_XRP/l_XRP)-1)*100
    b_XRP = float(XRP["bid"])
    p_XRP = b_XRP-value[3]
    
    ETH = ETH_stats()
    h_ETH = float(ETH["high"])
    l_ETH = float(ETH["low"])
    f_ETH = ((h_ETH/l_ETH)-1)*100
    b_ETH = float(ETH["bid"])
    p_ETH = b_ETH-value[4]
   
    
    print("\n")
    print("Posiadane zasoby:")
    for i in range(5):
        print(amount_currency[i],names[i],"kupione po cenie",value[i],"USD")
    print("\n")
    
    w = amount_currency[0]*value[0] + amount_currency[1]*value[1] + amount_currency[2]*value[2] + amount_currency[3]*value[3] + amount_currency[4]*value[4]
    s = amount_currency[0]*b_BTC + amount_currency[1]*b_LTC + amount_currency[2]*b_BCH + amount_currency[3]*b_XRP +amount_currency[4]*b_ETH
    p = ((s/w)-1)*100
    
    if s > w:
        print("Po wykonaniu operacji wzrost ilości USD o",p,"%")
    elif w >s:
        print("Po wykonaniu operacji spadek ilości USD o",p,"%")
    elif w == s:
        print("Po wykonaniu operacji brak zmian w ilości USD")
    
    print("\n")
    print(s)
    
    print("\n")
    print("Potencjalna zmiana na każdej z walut:")
    print("BTC",f_BTC,"%")
    print("LTC",f_LTC,"%")
    print("BCH",f_BCH,"%")
    print("XRP",f_XRP,"%")
    print("ETH",f_ETH,"%")
    
    print("\n")
    print("Zmiana na jedynm BTC ",p_BTC)
    print("Zmiana na jedynm LTC ",p_LTC)
    print("Zmiana na jedynm BCH ",p_BCH)
    print("Zmiana na jedynm XRP ",p_XRP)
    print("Zmiana na jedynm ETH ",p_ETH)
        
    
    cryp = xlwt.Workbook(encoding="utf-8")
    
    sheet1 = cryp.add_sheet("Crypto")
    
    sheet1.write(1, 1, "Posiadane zasoby")
    sheet1.write(2, 1, "BTC")
    sheet1.write(2, 2, amount_currency[0])
    sheet1.write(3, 1, "LTC")
    sheet1.write(3, 2, amount_currency[1])
    sheet1.write(4, 1, "BCH")
    sheet1.write(4, 2, amount_currency[2])
    sheet1.write(5, 1, "XRP")
    sheet1.write(5, 2, amount_currency[3])
    sheet1.write(6, 1, "ETH")
    sheet1.write(6, 2, amount_currency[4])
    sheet1.write(7, 1, "Zmiany")
    sheet1.write(8, 1, "BTC")
    sheet1.write(8, 2, f_BTC)
    sheet1.write(9, 1, "LTC")
    sheet1.write(9, 2, f_LTC)
    sheet1.write(10, 1, "BCH")
    sheet1.write(10, 2, f_BCH)
    sheet1.write(11, 1, "XRP")
    sheet1.write(11, 2, f_XRP)
    sheet1.write(12, 1, "ETH")
    sheet1.write(12, 2, f_ETH)
    
    cryp.save("crypto.xls")
    
crypto()

