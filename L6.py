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

end = False
while not end:
    print("Chose: ")
    print("add - Add resource")
    print("remove - Remove resource")
    print("show - Show wallet in USD")
    print("quit - Quit")
    choice = str(input())
    if choice == 'quit':
        break
    elif choice == 'add':
        resource_name_to_add = input("Name of resource: ")
        resource_amount_to_add = input("Amount of resource: ")
        add_resources(resource_name_to_add,int(resource_amount_to_add))
    elif choice == 'remove':
        resource_name_to_remove = input("Name of resource: ")
        resource_amount_to_remove = input("Amount of resource: ")
        add_resources(resource_name_to_remove,-int(resource_amount_to_remove))
    elif choice == 'show':
        print(wallet())

resources.to_csv('resources.csv',index=False)