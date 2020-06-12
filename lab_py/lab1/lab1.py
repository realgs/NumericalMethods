import numpy as np

A = np.random.randint(100, size=10)

def s_sort(A):
    A.sort()
    return A


def s_sorted(A):
    return sorted(A)

print(s_sort(A))
print(s_sorted(A))
