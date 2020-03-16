def selection_sort(to_sort):
    for j in range(len(to_sort)):
        x=j
        for i in range(len(to_sort)):
            if to_sort[i]<to_sort[x] and i>j:
                x=i
        if x!=j:
            to_sort[x] -= to_sort[j]
            to_sort[j] += to_sort[x]
            to_sort[x] = to_sort[j] - to_sort[x]
    return to_sort