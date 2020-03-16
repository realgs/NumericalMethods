def bubbleSort(numbersToSort):
    while True:
        Flag = False
        for i in range(len(numbersToSort) - 1):
            if numbersToSort[i] > numbersToSort[i + 1]:
                numbersToSort[i], numbersToSort[i + 1] = numbersToSort[i + 1], numbersToSort[i]
                Flag = True
        if not Flag:
            return numbersToSort


numbers = [10, 55, 2, 6, 7, 22, 101]

print(numbers)

sortedNumbers = bubbleSort(numbers)

print(sortedNumbers)


