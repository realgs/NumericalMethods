import random

A=[]
for i in range(15):
    A.append(random.randint(-50,50))

def babel(A):
    for i in range(len(A)):
        for j in range(len(A)-1):
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]

print(A)
babel(A)
print(A)