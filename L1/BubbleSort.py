from random import randint


def data(start,stop,size):
    lista = []
    for i in range(int(size)):
        nl = randint(start, stop)
        lista.append(nl)
    return lista


def bubblesort(data):
    nd = data[:]
    for i in range(len(nd) - 1, 0, -1):
        for j in range(i):
            if nd[j] > nd[j + 1]:
                nd[j], nd[j + 1] = nd[j + 1], nd[j]
    return nd


a = data(10, 100, 10)
sorted_numbers = bubblesort(a)
print(a, 'data')
print(sorted_numbers, 'sorted')
