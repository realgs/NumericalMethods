def bubbleSort(numbersToSort):
    Flag = True
    while Flag:
        Flag = False
        for i in range(len(numbersToSort) - 1):
            if numbersToSort[i] > numbersToSort [i + 1]:
                numbersToSort[i], numbersToSort[i + 1] = numbersToSort[i + 1], numbersToSort[i]
                Flag = True


numbers = [10, 55, 2, 6, 7, 22, 101]

print(numbers)

bubbleSort(numbers)

print(numbers)