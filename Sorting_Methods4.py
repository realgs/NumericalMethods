import time

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


def selection(liczby):
    n = len(liczby)
    for i in range(n):
        lowest = i
        for j in range(i+1,n):
            if liczby[j] < liczby[lowest]:
                lowest = j

        liczby[i],liczby[lowest] = liczby[lowest], liczby[i]

    return liczby


def Mergesort(liczby):
    if len(liczby) > 1:
        middle = len(liczby) // 2
        left = liczby[:middle]
        right = liczby[middle:]

        Mergesort(left)
        Mergesort(right)
        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                liczby[k] = left[i]
                i = i+1
            else:
                liczby[k] = right[j]
                j = j+1
            k = k+1

        while i < len(left):
            liczby[k] = left[i]
            i = i+1
            k = k+1
        while j < len(right):
            liczby[k] = right[j]
            j = j+1
            k = k+1
    return liczby





