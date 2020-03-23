import random
import time as t


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


def SelectionSort(tablica):
    for i in range(len(tablica)):
        indeks_min = i
        for j in range(i+1, len(tablica)):
            if tablica[indeks_min] > tablica[j]:
                indeks_min = j
        tablica[i], tablica[indeks_min] = tablica[indeks_min], tablica[i]
    return tablica


def IleCzasu(funkcja):
   start = t.time()
   funkcja(tablica)
   stop = t.time()
   czas = stop - start
   return czas


def Porownanie():
    funkcje = [InsertSort, QuickSort, BubbleSort, SelectionSort]
    czasy = []
    for funkcja in funkcje:
        czasy.append(IleCzasu(funkcja))

    zestawienie = dict(zip(czasy, funkcje))
    min_czas = min(zestawienie.keys())
    return [zestawienie[min_czas].__name__, min_czas]


liczby_testowe = random.sample(range(-10000, 10000), 15)
tablica = liczby_testowe.copy()


print('\nTablica przed sortowaniem:', tablica)
print('\nNajszybszą z funkcji jest:', Porownanie()[0]+', a zadaną listę sortuje w czasie:', Porownanie()[1], 'sekund')
print('\nTablica po sortowaniu:', tablica)