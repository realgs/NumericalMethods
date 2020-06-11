# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:55:51 2020

@author: piotr
"""

def merg(a,p,q,r):
    
    p2 = p
    r2 = r
    
    A = a[p:q+1]
    B = a[q+1:r+1]
    C = [] 
    #print(p,q,r,A,B)
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
    #print(C)   
    a[p2:r2+1] = C    
            
def sort (a,p,r):
    if p < r:
        q = (p+r)//2
        sort(a,p,q)
        sort(a,q+1,r)
        merg(a,p,q,r)
    
        
        

a=[12, 11, 13, 5, 6, 7,10,41,23,4] 

sort(a,0,len(a)-1)
print(a)