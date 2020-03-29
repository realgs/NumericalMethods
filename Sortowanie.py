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

liczby = [-2324, 1, 3, 543, -1, 0, 5, 124, 12412, 0]
tablica = liczby.copy()

print(BubbleSort(tablica))
print(QuickSort(tablica))

