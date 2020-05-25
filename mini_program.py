import pandas as pd
import requests

resources = pd.read_csv("resources.csv")

def wallet():
    sum=0
    for i in resources:
        response = requests.get('https://bitbay.net/API/Public/'+i+'USD/trades.json?sort=desc')
        if response.json() == []:
            response = requests.get('https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-'+i+'&type=both')
            price = response.json()['result']['buy'][0]['Rate']
            sum+=price*resources[i]
        else:
            price = response.json()[0]['price']
            sum+=price*resources[i]
    return int(sum)

def add_resources(resource_name,amount):
    if resource_name in resources:
        resources[resource_name]+=amount
    else:
        response = requests.get('https://bitbay.net/API/Public/'+resource_name+'USD/trades.json?sort=desc')
        if response.json()==[]:
            response = requests.get('https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-'+resource_name+'&type=both')
            if response.json()==[]:
                print("Error: "+resource_name+" doesn\'t exist")
            resources[resource_name]=amount
        resources[resource_name]=amount

done = False
while not done:
    print("Chose: ")
    print("1. Add resource")
    print("2. Remove resource")
    print("3. Show wallet in USD")

    print("0. Quit")
    choice = int(input())
    if choice == 0:
        break
    elif choice == 1:
        resource_name_to_add = input("Name of resourc: ")
        resource_amount_to_add = input("Amount of resourc: ")
        add_resources(resource_name_to_add,int(resource_amount_to_add))
    elif choice == 2:
        resource_name_to_remove = input("Name of resourc: ")
        resource_amount_to_remove = input("Amount of resourc: ")
        add_resources(resource_name_to_remove,-int(resource_amount_to_remove))
    elif choice == 3:
        print(wallet())

resources.to_csv('resources.csv',index=False)
