import random as rd

def create_tab(size,start,stop):
    tab=[]
    for i in range(int(size)):
        nb=rd.randint(start,stop)
        tab.append(nb)
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

