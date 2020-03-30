import time
x=[4,34,6,12,7,8,9]


def sort_wstaw(x):
    zbior1=x
    start = time.time()
    for i in range(len(x)):
        o = zbior1[i]
        j = i - 1
        while j>=0 and zbior1[j]>o:
            zbior1[j + 1] = zbior1[j]
            j = j - 1
        zbior1[j + 1] = o
    end = time.time()
    sortwstawianie=end-start
    return zbior1,sortwstawianie

sow=sort_wstaw(x)
print(sow)

def sort_babe(x):
    zbior2=x
    start = time.time()
    for t in range(len(x)-1):
        for y in range(len(x)-1):
            if zbior2[y]>zbior2[y+1]:
                z=zbior2[y]
                zbior2[y]=zbior2[y+1]
                zbior2[y+1]=z
    end = time.time()
    sortbabelkowe=end-start
    return zbior2,sortbabelkowe

sob=sort_babe(x)
print(sob)

def sort_wyb(x):
    zbior4=x
    i = 0
    start=time.time()
    while i < len(x) - 1:
        min_l=i
        for j in range(i + 1, len(x)):
            if zbior4[j] < zbior4[min_l]:
                min_l = j
        a=zbior4[min_l]
        zbior4[min_l]=zbior4[i]
        zbior4[i]=a
        i+=1
    end=time.time()
    selection=end-start
    return zbior4,selection

sel=sort_wyb(x)
print(sel)

def sort_quick(x):
    left = []
    center = []
    right = []

    if len(x) > 1:
        pivot = x[0]

        for n in x:
            if n < pivot:
                left.append(n)
            elif n > pivot:
                right.append(n)
            else:
                center.append(n)
        return sort_quick(left) + center + sort_quick(right)
    else:
        return x
start = time.time()
result_sort_quick = sort_quick(x)
qui = (result_sort_quick, time.time() - start)
print(qui)   


def porownanie(op,on,om,od):
    return(min(op,on,om,od))
por=porownanie(sow[1],sob[1],sel[1],qui[1])
print(por)