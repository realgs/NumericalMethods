import time
from bubbleSort import bubbleSort
from selectionSort import selectionSort
from mergeSort import mergeSort
from QuickSort import quickSortHelper

numbers = [10, 55, 61, 102, 234, 12, 5, 79, 340, 123, 5467, 2341, 6, 72, 54, 1, 456]
print("Numbers to sort: {}".format(numbers))
print(40*"=")


def timer(sortingFunction):

    start = time.perf_counter()
    sortingFunction(numbers)
    end = time.perf_counter()

    elapsed_time = end - start

    return elapsed_time

bubble_time = timer(bubbleSort)
selection_time = timer(selectionSort)
merge_time = timer(mergeSort)
quick_time = timer(quickSortHelper)

print("Bubble Sort:\nresult: {}\ntime: {}".format(bubbleSort(numbers), timer(bubbleSort)))
print(40*"=")
print("Selection Sort:\nresult: {}\ntime: {}".format(selectionSort(numbers), timer(selectionSort)))
print(40*"=")
print("Merge Sort:\nresult: {}\ntime: {}".format(mergeSort(numbers), timer(mergeSort)))
print(40*"=")
print("Quick Sort:\nresult: {}\ntime: {}".format(quickSortHelper(numbers), timer(quickSortHelper)))
print(40*"=")

print("Sorting times ascednging: ")
times_sorted = bubbleSort([bubble_time, selection_time, merge_time, quick_time])
print(times_sorted)

