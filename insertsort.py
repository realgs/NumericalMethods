def insertsort(tab):
    for i in range(len(tab)):
        k=tab[i]
        j=i-1
        while j>=0 and tab[j]>k:
            tab[j+1]=tab[j]
            j=j-1
            tab[j+1]=k
    return tab

c=insertsort([23,4,87,42,0,12,3,1,1,23])
print(c)