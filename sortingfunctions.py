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


def time_count(function, tab):
    start = t.time()
    function(tab)
    stop = t.time()
    return stop - start, tab


def comparision():
    pass

if __name__ == "__main__":
    # quick = test.copy()
    # quick_sort(quick, 0, len(test) - 1)
    # bubble = bubble_sort(test.copy())
    # insert = insertion_sort(test.copy())
    # select = selection_sort(test.copy())
    #
    # print('Tablica do posortowania:', test)
    # print('Bubble sort:', bubble)
    # print('Quick sort: ', quick)
    # print('Insertion sort:', insert)
    # print('Selection sort:', select)
    quick = comparision(quick_sort, test.copy())
    bubble = comparision(bubble_sort, test.copy())
    insertion = comparision(insertion_sort, test.copy())
    selection = comparision(selection_sort, test.copy())
    print('Czas quick sort:', quick[0])
    print('Czas bubble sort:', bubble[0])
    print('Czas insertion sort:', insertion[0])
    print('Czas selection sort:', selection[0])
