import numpy as np
import time as t


def bubble_sort(array):
    length = len(array)
    for i in range(length):
        for j in range(0, length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def selection_sort(array):
    length = len(array)
    i = 0
    while i < length - 1:
        min_idx = i
        for j in range(i + 1, length):
            if array[j] < array[min_idx]:
                min_idx = j
        array[min_idx], array[i] = array[i], array[min_idx]
        i += 1
    return array


def partition(array, left, right):
    i = left - 1
    pivot = array[right]
    for j in range(left, right):
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[right], array[i + 1] = array[i + 1], array[right]
    return i + 1


def quick_sort(array, left=0, right=None):
    if not right:
        right = len(array) - 1
    if left < right:
        index = partition(array, left, right)
        quick_sort(array, left, index - 1)
        quick_sort(array, index + 1, right)


def insertion_sort(array):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while key < array[j] and j >= 0:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


def comparison(function, tab):
    start = t.time()
    function(tab)
    stop = t.time()
    return stop - start, tab


if __name__ == "__main__":
    test = [12, 5, 4, 7, -5, -10, 12, 4, 8, 16, 15, 2]
    quick = comparison(quick_sort, test.copy())
    bubble = comparison(bubble_sort, test.copy())
    insertion = comparison(insertion_sort, test.copy())
    selection = comparison(selection_sort, test.copy())
    print("Tablica przed posortowaniem: {}".format(test))
    print('Czas quick sort:', quick[0],'\nTablica:',quick[1])
    print('Czas bubble sort:', bubble[0],'\nTablica:',bubble[1])
    print('Czas insertion sort:', insertion[0],'\nTablica:',insertion[1])
    print('Czas selection sort:', selection[0],'\nTablica:',selection[1])
