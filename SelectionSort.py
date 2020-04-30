# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:33:38 2020

@author: piotr
"""

def sort(a):
    for i in range (len(a)):
        minimum = i
        
        for j in range (i+1, len(a)):
            if a[j] < a[minimum]:
                minimum = j
                
        a[minimum], a[i] = a[i], a[minimum]
     

a=[4,8,1,9,2,3]
sort(a)
print(a)
'''
def sort(a):        
    for i in range(len(a)):
        mini = i
        
        for j in range(i + 1, len(a)):
          
            if a[j] < a[mini]:
                mini = j
   
        a[mini], a[i] = a[i], a[mini]            

a=[4,8,1,9,2,3]
sort(a)
print(a)'''