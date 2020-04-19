


def sortowanie_bąbelkowe(liczby):
    n = len(liczby)
    zmieniona = True
    while zmieniona == True:
        zmieniona = False
        for i in range(n-1):
            if liczby[i] > liczby[i+1]:
                liczby[i], liczby[i+1] = liczby[i+1],liczby[i]
                zmieniona = True
    return liczby

lista = [1,4,6,2,3,7,5,8]
sortowanie_bąbelkowe(lista)
print(lista, 'bąbelkowe')

def przez_wstawianie(liczby):
    n = len(liczby)
    for i in range(1,n):
        wstawianie = liczby[i]
        j = i - 1
        while j >= 0 and liczby[j] > wstawianie:
            liczby[j+1] = liczby[j]
            j = j - 1
        liczby[j+1] = wstawianie
    return(liczby)

lista = [3,2,6,5,4,9,1,5,4]
przez_wstawianie(lista)
print(lista,'przez wstawianie')

