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

def main(size,start,stop):
    unsorted_tab=create_tab(size,start,stop)
    print('Before sorting: ',unsorted_tab)
    sorted_tab=bubble_sort(unsorted_tab)
    print('After sorting: ',sorted_tab)

main(10,1,10)


