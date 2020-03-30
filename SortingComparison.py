from random import randint
from timeit import timeit


def data(start,stop,size):
    lista = []
    for i in range(int(size)):
        nl = randint(start, stop)
        lista.append(nl)
    return lista


def bubblesort(data):
    nd = data[:]
    start = timeit()
    for i in range(len(nd) - 1, 0, -1):
        for j in range(i):
            if nd[j] > nd[j + 1]:
                nd[j], nd[j + 1] = nd[j + 1], nd[j]
    stop = timeit()
    time = abs(stop - start)
    return [nd,time]


def selectionSort(data):
    nd = data[:]
    start = timeit()
    for i in range(len(nd)):
        currentMin = i
        for j in range(i + 1, len(nd)):
            if nd[j] < nd[currentMin]:
                currentMin = j
        nd[currentMin], nd[i] = nd[i], nd[currentMin]
    stop = timeit()
    time=abs(stop-start)
    return [nd,time]


def shellSort(data):
    nd = data[:]
    start = timeit()
    gap = len(nd) // 2
    while gap > 0:
        for i in range(gap, len(nd)):
            temp = nd[i]
            j = i
            while j >= gap and nd[j - gap] > temp:
                nd[j] = nd[j - gap]
                j = j - gap
            nd[j] = temp
        gap = gap // 2
    stop = timeit()
    time = abs(stop - start)
    return [nd,time]


def insertionsort(data):
    nd=data[:]
    start = timeit()
    for i in range(1, len(nd)):
        j = i - 1
        nxt_element = nd[i]
        while (nd[j] > nxt_element) and (j >= 0):
            nd[j + 1] = nd[j]
            j = j - 1
        nd[j + 1] = nxt_element
    stop = timeit()
    time = abs(stop - start)
    return [nd, time]


def compare():
    names = ['bubblesort','shellSort','selectionSort','insertionsort']
    times = [bubblesort(a)[1],shellSort(a)[1],selectionSort(a)[1],insertionsort(a)[1]]
    sorted = [bubblesort(a)[0],shellSort(a)[0],selectionSort(a)[0],insertionsort(a)[0]]

    minimum = min(times)
    index_min = times.index(minimum)
    name_f = names[index_min]
    sorted_numbs = sorted[index_min]

    return [minimum,name_f,sorted_numbs]


a = data(10, 100, 10)
print('input data',a)
print('output data',compare()[2],'\n')
print('function called',compare()[1],'was the best')
print('and did it in ',compare()[0],'s')
