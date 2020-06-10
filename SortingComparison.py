import random as rd
import time

def create_tab(size,start,stop):
    tab=[]
    for i in range(int(size)):
        nb=rd.randint(start,stop)
        tab.append(nb)
    return tab

def insert_sort(tab):
    for i in range(1,len(tab)):
        nb = tab[i]
        j = i - 1
        while j >= 0 and tab[j] > nb:
            tab[j+1] = tab[j]
            j = j - 1
        tab[j+1] = nb
    return tab

def bubble_sort(tab):
    for i in range(len(tab)):
        j=len(tab)-1
        while j>i:
            if tab[j]<tab[j-1]:
                mem=tab[j]
                tab[j]=tab[j-1]
                tab[j-1]=mem
            j-=1
    return tab

def quick_sort(tab):
    smaller = []
    equal = []
    bigger = []
    if len(tab) > 1:
        pivot = tab[0]
        for nb in tab:
            if nb < pivot:
                smaller.append(nb)
            elif nb == pivot:
                equal.append(nb)
            else:
                bigger.append(nb)
        return quick_sort(smaller)+equal+quick_sort(bigger)
    else:
        return tab
    
def selection_sort(tab):
    for i in range(len(tab)):
        minimum = min(tab[i:]) 
        min_index = tab[i:].index(minimum) 
        tab[i + min_index] = tab[i] 
        tab[i] = minimum                  
    return tab

def count_time():
    tab=create_tab(2000,1,10000)
    functions=[insert_sort,bubble_sort,quick_sort,selection_sort]
    function=['insert_sort','bubble_sort','quick_sort','selection_sort']
    times={}
    for i in range(len(functions)):
        start=time.time()
        functions[i](tab)  
        stop=time.time()
        czas=stop-start
        times[function[i]]=czas
    time_list=list(times.values()) 
    min_time=min(time_list)
    max_time=max(time_list)
    return print('Czasy realizacji:\n',times,'\nCzas minimalny:',min_time,'\nCzas maksymalny:',max_time)
     
count_time()




    
    
    
    
    
