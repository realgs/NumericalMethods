import random

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

A=[]
for i in range(15):
    A.append(random.randint(-50,50))
print(A)
print(quick_sort(A))