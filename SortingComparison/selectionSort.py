def selectionSort(numbersToSort):
    for i in range(len(numbersToSort)):
        currentMin = i
        for j in range(i + 1, len(numbersToSort)):
            if numbersToSort[j] < numbersToSort[currentMin]:
                currentMin = j
        numbersToSort[currentMin], numbersToSort[i] = numbersToSort[i], numbersToSort[currentMin]
    return numbersToSort