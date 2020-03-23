import random

def BubbleSort(tablica):
    n = len(tablica)
    while n > 1:
        for i in range(n-1):
            if tablica[i] > tablica[i+1]:
                tablica[i], tablica[i+1] = tablica[i+1], tablica[i]
        n -= 1
    return tablica

def QuickSort(tablica):

    mniejsze = []
    rowne = []
    wieksze = []

    if len(tablica) > 1:
        piwot = tablica[0]
        for element in tablica:
            if element < piwot:
                mniejsze.append(element)
            elif element == piwot:
                rowne.append(element)
            else:
                wieksze.append(element)
        return QuickSort(mniejsze) + rowne + QuickSort(wieksze)
    else:
        return tablica

def InsertSort(tablica):
    for i in range(1, len(tablica)):
        wstawiany = tablica[i]
        j = i - 1
        while j >= 0 and tablica[j] > wstawiany:
            tablica[j+1] = tablica[j]
            j -= 1
        tablica[j+1] = wstawiany
    return tablica


liczby_testowe = random.sample(range(-10000, 10000), 15)
tablica = liczby_testowe.copy()

