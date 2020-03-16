# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:58:08 2020

@author: piotr
"""

a = [9,1,9,5,7,2,1,3,9,6,3,2,6,9]

def sort (a):
    for i in range (1,len(a)):
        z = a[i]
        j = i-1
        while j >= 0 and a[j] > z:
            a [j + 1] = a[j]
            j = j - 1
        a[j + 1] = z
        
sort(a)
print(a)