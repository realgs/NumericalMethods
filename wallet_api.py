import content as c


def main(response):
    user = c.load_user_data()
    msg = '1. Dodaj walutę\n2. Edytuj/usuń walutę\n3. Uaktualnij wycenę\n4. Dodaj nowy klucz API\n5. Usuń klucz API\n'
    msg += '6. Uaktualnij markety\n7. Wyceń portfel\n8. Wyjście z programu\n'
    while True:
        c.show(user)
        print('\nMenu')
        print(msg)
        try:
            choice = int(input("Wprowadź cyfrę (1-8): "))
        except ValueError:
            print("Wprowadzono niewłaściwy wybór!")
            main(response)
        if not 0 < choice < 9:
            print('Wprowadzono niewłaściwą cyfrę!')
            main(response)
        if choice == 1:
            user = c.wyb1(user, response)
        elif choice == 2:
            user = c.wyb2(user)
        elif choice == 3:
            user = c.wyb3(user, response)
        elif choice == 4:
            c.wyb4()
        elif choice == 5:
            c.wyb5()
        elif choice == 6:
            response = c.wyb6()
        elif choice == 7:
            values = c.wyb7(user, response)
            if len(values) > 1:
                mess = "\n\nObecna wartość portfela w {} wynosi: {}.\nObecny bilans wynosi: {}\n"
                mess = mess.format(values[2], values[0], values[0] - values[1])
                print(mess)
            else:
                print("Baza pusta! Operacja niedozwolona!\n")

        else:
            confirm = input('Aby zamknąć wpisz "q":')
            if confirm == 'q':
                c.save_user(user)
                return 0


if __name__ == '__main__':
    response = c.load_markets()
    main(response)
