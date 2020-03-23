def bubbleSort(numbersToSort):
    while True:
        Flag = False
        for i in range(len(numbersToSort) - 1):
            if numbersToSort[i] > numbersToSort[i + 1]:
                numbersToSort[i], numbersToSort[i + 1] = numbersToSort[i + 1], numbersToSort[i]
                Flag = True
        if not Flag:
            return numbersToSort



