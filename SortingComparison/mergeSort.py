def Merge(left_half, right_half):
    sortedList = []
    l_index = r_index = 0

    for _ in range(len(left_half)+len(right_half)):
        if l_index < len(left_half) and r_index < len(right_half):

            if left_half[l_index] <= right_half[r_index]:
                sortedList.append(left_half[l_index])
                l_index += 1
            else:
                sortedList.append(right_half[r_index])
                r_index += 1

        elif l_index == len(left_half):
            sortedList.append(right_half[r_index])
            r_index += 1

        elif r_index == len(right_half):
            sortedList.append(left_half[l_index])
            l_index += 1

    return sortedList


def mergeSort(numbersToSort):
    if len(numbersToSort) <= 1:
        return numbersToSort

    middle = len(numbersToSort) // 2

    l_list = mergeSort(numbersToSort[:middle])
    r_list = mergeSort(numbersToSort[middle:])

    return Merge(l_list, r_list)




