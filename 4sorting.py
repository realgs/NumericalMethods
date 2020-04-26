import time
tab=[15,23,0,23,45,1,1,0]

def sortbabel(tab):
    start=time.time()
    
    for i in range(len(tab)-1):
        for i in range(len(tab)-1):
            if tab[i]>tab[i+1]:
                a=tab[i]
                tab[i]=tab[i+1]
                tab[i+1]=a
                
    finish=time.time()
    t1=finish-start
    return tab,t1

def insertsort(tab):
    start=time.time()
    
    for i in range(len(tab)):
        k=tab[i]
        j=i-1
        while j>=0 and tab[j]>k:
            tab[j+1]=tab[j]
            j=j-1
            tab[j+1]=k
            
    finish=time.time()
    t2=finish-start
    return tab,t2

def selectsort(tab):
    start=time.time()
    n=len(tab)
    i=0
    while i<n-1:
        minE=i
        for j in range(i+1,n):
            if tab[j]<tab[minE]:
                minE=j
        a=tab[minE]
        tab[minE]=tab[i]
        tab[i]=a
        i+=1
    
    finish=time.time()
    t3=finish-start
    return tab,t3

def sortquick(tab):
    n=len(tab)
    left = []
    center = []
    right = []

    if n > 1:
        pivot = tab[0]

        for n in tab:
            if n < pivot:
                left.append(n)
            elif n > pivot:
                right.append(n)
            else:
                center.append(n)
        return sortquick(left) + center + sortquick(right)
    else:
        return tab

def comparison(t1,t2,t3,t4):
    return(min(t1,t2,t3,t4))


b=sortbabel(tab)
print("bubblesort",b)

c=insertsort(tab)
print("insertsort",c)

d=selectsort(tab)
print("selectsort",d)

start = time.time()
result_sort_quick = sortquick(tab)
t4=time.time() - start
e = ("quicksort",result_sort_quick,t4)
print(e)


f=comparison(b[1],c[1],d[1],e[2])
print("shortest_time",f)