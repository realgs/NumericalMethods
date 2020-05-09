import content as c


def main(response):
    user = c.load_user_data() if c.load_user_data() else None
    msg = '1. Dodaj walutę\n2. Usuń walutę\n3. Uaktualnij wycenę\n4. Dodaj nowy klucz API\n5. Usuń klucz API\n'
    msg += '6. Uaktualnij markety\n7. Wyceń portfel\n8. Wyjście z programu\n'
    while True:
        try:
            choice = int(input("Wprowadź cyfrę (1-8): "))
        except ValueError:
            print("Wprowadzono niewłaściwy wybór!")
            main(response)
        if not 0 < choice < 9:
            print('Wprowadzono niewłaściwą cyfrę!')
            main(response)
        if choice == 1:
            c.wyb1()
        elif choice == 2:
            c.wyb2()
        elif choice == 3:
            c.wyb3()
        elif choice == 4:
            c.wyb4()
        elif choice == 5:
            c.wyb5()
        elif choice == 6:
            response = c.wyb6()
        elif choice == 7:
            c.wyb7()
        else:
            confirm = input('Aby zamknąć wpisz "q":')
            if confirm == 'q':
                c.save_user_data()
                return 0


if __name__ == '__main__':
    response = c.load_markets()
    main(response)
