import time

def merg(a,p,q,r):
    
    p2 = p
    r2 = r
    
    A = a[p:q+1]
    B = a[q+1:r+1]
    C = [] 
    
    i = 0 
    j = 0
    
    while(len(C) < len(A)+len(B)):
        if i > len(A)-1:
            while (j < len(B)):
                C.append(B[j])
                j+=1
            break
            
        if j > len(B)-1:
            while (i < len(A)):
                C.append(A[i])
                i+=1
            break
                
        if A[i] <= B[j]:
            C.append(A[i])
            i+=1
        else:
            C.append(B[j])
            j+=1
 
    a[p2:r2+1] = C    
            
def sort (a,p,r):
    if p < r:
        q = (p+r)//2
        sort(a,p,q)
        sort(a,q+1,r)
        merg(a,p,q,r)
    
def sort2(a):
    for i in range (len(a)):
        minimum = i
        
        for j in range (i+1, len(a)):
            if a[j] < a[minimum]:
                minimum = j
                
        a[minimum], a[i] = a[i], a[minimum]
################################################# PORÓWNANIE    

start_time = time.time()
for i in range(100000):
    a=[12, 11, 13, 5, 6]
    sort(a,0,len(a))    
print("---MergSort time: %s seconds ---" % (time.time() - start_time))

start_time = time.time()
for i in range(100000):
    a=[12, 11, 13, 5, 6]
    sort2(a)    
print("--SelectionSort time:- %s seconds ---" % (time.time() - start_time))
