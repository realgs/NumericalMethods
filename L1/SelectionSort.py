from random import randint


def data(start,stop,size):
    lista = []
    for i in range(int(size)):
        nl = randint(start,stop)
        lista.append(nl)
    return lista


def selectionSort(data):
    nd = data[:]
    for i in range(len(nd)):
        currentMin = i
        for j in range(i + 1, len(nd)):
            if nd[j] < nd[currentMin]:
                currentMin = j
        nd[currentMin], nd[i] = nd[i], nd[currentMin]
    return nd


a = data(10,100,10)
sorted_numbers = selectionSort(a)
print(a,'data')
print(sorted_numbers,'sorted')
