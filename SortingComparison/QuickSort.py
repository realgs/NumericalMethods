def partition(numbersToSort, low, high):
    pivot = numbersToSort[(low + high) // 2]
    i = low - 1
    j = high + 1

    while True:
        i += 1

        while numbersToSort[i] < pivot:
            i += 1

        j -= 1
        while numbersToSort[j] > pivot:
            j -= 1

        if i >= j:
            return j

        numbersToSort[i], numbersToSort[j] = numbersToSort[j], numbersToSort[i]
def quickSortHelper(numbersToSort):

    def quickSort(items, low, high):
        if low < high:

            split = partition(items, low, high)
            quickSort(items, low, split)
            quickSort(items, split + 1, high)

    quickSort(numbersToSort, 0, len(numbersToSort) - 1)

    return numbersToSort
