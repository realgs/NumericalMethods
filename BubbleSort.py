# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 12:47:40 2020

@author: piotr
"""
def swap(a,i,j):
    zp = a[i]
    a[i] = a[j]
    a[j] = zp    

a = [8,1,9,6,3,4,5]
 
def sort (a):
    n = len(a)
  
    for j in range (n):
        for i in range (n-1):
            if a[i] > a[i+1]:
                swap(a,i,i+1)
sort(a)
print(a)