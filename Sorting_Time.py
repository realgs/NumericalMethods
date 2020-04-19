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


def Timer(list,function):
    start = time.time()
    function(list)
    end = time.time()
    timer = end - start
    return timer

def Time_Comparison(liczby):

    czasy = {}
    timer = Timer(liczby,sortowanie_bąbelkowe)
    czasy.update({'bubble sort': timer})
    timer = Timer(liczby,przez_wstawianie)
    czasy.update({'Insertion sort': timer})
    timer = Timer(liczby,selection)
    czasy.update({'selection sort':timer})
    timer = Timer(liczby,Mergesort)
    czasy.update({'Merge sort':timer})
    return czasy


liczby = [9,1,25,17,80,290,50,3,75,8]
czasy = Time_Comparison(liczby)
print('sorting times:\n',czasy)
print('Fastest sorting ==========>',min(czasy))
print('Slowest sorting ==========>',max(czasy))

