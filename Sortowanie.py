def BubbleSort(dane):
    n = len(dane)
    while n > 1:
        for i in range(n-1):
            if dane[i] > dane[i+1]:
                dane[i], dane[i+1] = dane[i+1], dane[i]
        n -= 1
    return dane

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
