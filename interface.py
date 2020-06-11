from code import input_your_cryptos, percentage_check, value_check_USD, value_check_EUR, deleting_resource, \
                 adding_resource, changing_quantity, resource_check, clear_resources, check_if_empty


def interface():
    while True:
        print(40 * "=")
        print("Actions: \n"
              "'1': Entering the resources. WARNING! This option wipes the previous data.\n"
              "'2': Resource check\n"
              "'3': Percentage check\n"
              "'4': Value check\n"
              "'5': Add a resource\n"
              "'6': Delete a resource\n"
              "'7': Edit quantity of a resource\n"
              "'8': Clear all resources\n"
              "'Q: Quit")
        print(40 * "=")

        action = input("Choose an action: ")

        if action == '1':
            input_your_cryptos()
        elif action == '2':
            if check_if_empty() is True:
                print("You don't have any resources")
            else:
                resource_check()
        elif action == '3':
            if check_if_empty() is True:
                print("You don't have any resources")
            else:
                percentage_check()
        elif action == '4':
            if check_if_empty() is True:
                print("You don't have any resources")
            else:
                currency = input("Which currency would you prefer? USD or EUR: ").upper()
                if currency == 'USD':
                    value_check_USD()
                elif currency == 'EUR':
                    value_check_EUR()
                else:
                    print("Wrong input")
        elif action == '5':
            adding_resource()
        elif action == '6':
            if check_if_empty() is True:
                print("You don't have any resources")
            else:
                deleting_resource()
        elif action == '7':
            if check_if_empty() is True:
                print("You don't have any resources")
            else:
                changing_quantity()
        elif action == '8':
            clear_resources()
        elif action.upper() == 'Q':
            break
        else:
            print("You have entered a wrong character")
