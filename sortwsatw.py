def sortwstaw(x):
    for i in range(len(x)):
        o = x[i]
        j = i - 1
        while j>=0 and x[j]>o:
            x[j + 1] = x[j]
            j = j - 1
        x[j + 1] = o
    return x