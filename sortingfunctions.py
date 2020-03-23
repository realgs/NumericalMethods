import numpy as np
import time as t


def bubble_sort(array):
    copy = array[:]
    length = len(copy)
    for i in range(length):
        for j in range(0, length - i - 1):
            if copy[j] > copy[j + 1]:
                copy[j], copy[j + 1] = copy[j + 1], copy[j]
    return copy


def partition(array, left, right):
    i = left - 1
    pivot = array[right]
    for j in range(left, right):
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[right], array[i + 1] = array[i + 1], array[right]
    return i + 1


def quick_sort(array, left, right):
    if left < right:
        index = partition(array, left, right)
        quick_sort(array, left, index - 1)
        quick_sort(array, index + 1, right)


def comparision(function, tab):
    start = t.time()
    function(tab)
    stop = t.time()
    return stop - start


if __name__ == "__main__":
    test = np.array([7, 5, 8, 4, 2, 7, 9, 0, 1, ])
    kopia = test[:]
    quick_sort(kopia, 0, len(test) - 1)
    print('Bubble sort:', bubble_sort(test))
    print('Quick sort: ', kopia)
    print('Tablica:    ', test)
