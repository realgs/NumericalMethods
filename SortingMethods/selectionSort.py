def selectionSort(numbersToSort):
    for i in range(len(numbersToSort)):
        currentMin = i
        for j in range(i + 1, len(numbersToSort)):
            if numbersToSort[j] < numbersToSort[currentMin]:
                currentMin = j
        numbersToSort[currentMin], numbersToSort[i] = numbersToSort[i], numbersToSort[currentMin]
    return numbersToSort

numbers = [10, 55, 2, 6, 7, 22, 101]

print(numbers)

print(selectionSort(numbers))