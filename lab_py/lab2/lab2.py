import time
import numpy as np

A = np.random.randint(2000, size=2000)

def s_sort(arr):
    start = time.time()
    arr.sort()
    end = time.time()
    print('Sort() time:', end-start)

def s_sorted(arr):
    start = time.time()
    sorted(arr)
    end = time.time()
    print('Sorted time:', end-start)


def insertionSort(arr):
    start = time.time()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >=0 and key < arr[j] :
                arr[j+1] = arr[j]
                j -= 1
        arr[j+1] = key
    end = time.time()
    print('Insertion Sort time:', end-start)

def bubbleSort(arr):
    start = time.time()
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

    end = time.time()
    print('Bubble Sort time:', end-start)


bubbleSort(A)
insertionSort(A)
s_sort(A)
s_sorted(A)
