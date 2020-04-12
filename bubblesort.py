def sortbabel(tab):
    for i in range(len(tab)-1):
        for i in range(len(tab)-1):
            if tab[i]>tab[i+1]:
                a=tab[i]
                tab[i]=tab[i+1]
                tab[i+1]=a
    return tab

b=sortbabel([2,32,1,0,34,324,532,2,19])
print(b)