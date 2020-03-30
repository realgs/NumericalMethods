import random
import time

#A = []
#for i in range(15):
#    A.append(random.randint(-50, 50))

def babel(A):
    for i in range(len(A)):
        for j in range(len(A)-1):
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]


def quick_sort(A):
    left=[]
    mid=[]
    right=[]

    if len(A)>1:
        select=A[0]
        for i in A:
            if i>select:
                right.append(i)
            elif i==select:
                mid.append(i)
            else:
                left.append(i)
        return quick_sort(left) + mid + quick_sort(right)
    else:
        return A

def selection_sort(A):
    for i in range(len(A)):

        min = i
        for j in range(i + 1, len(A)):
            if A[min] > A[j]:
                min = j

        A[i], A[min] = A[min], A[i]
    return A

def insert_sort(A):

    for i in range(1, len(A)):
        mark = A[i]
        j = i - 1
        while j >= 0 and mark < A[j]:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = mark
    return A


def time_measure(fun1,fun2):
    A = []
    for i in range(50):
        A.append(random.randint(-50, 50))
    t0 = int(round(time.time() * 1000))
    for i in range(10000):
        fun1(A)
    t1 = int(round(time.time() * 1000)) - t0
    #time1 = t1 - t0
    t2 = int(round(time.time() * 1000))
    for i in range(10000):
        fun2(A)
    t3 = int(round(time.time() * 1000)) - t2
    #time2 = t3-t2
    return t1, t3

#jako argument funkcji time_measure nalezy podac 2 nazwy funkcji sortowania
print(time_measure(quick_sort,insert_sort))
