def BubbleSort(dane):
    n = len(dane)
    while n > 1:
        for i in range(n-1):
            if dane[i] > dane[i+1]:
                dane[i], dane[i+1] = dane[i+1], dane[i]
        n -= 1
    return dane