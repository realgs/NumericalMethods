import numpy as np


def bubble_sort(array):
    copy = array[:]
    length = len(copy)
    for i in range(length):
        for j in range(0, length - i - 1):
            if copy[j] > copy[j + 1]:
                copy[j], copy[j + 1] = copy[j + 1], copy[j]
    return copy
