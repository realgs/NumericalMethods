import random as ran
print("Podaj z jakiego zakresu losujemy elementy do tabeli.")
x=int(input("Losujemy od: "))
y=int(input("Losujemy do: "))
tab=[]

for i in range(0,ran.randint(0,40)):
    tab.append(ran.randint(x,y))
print("Nasza tablica:",tab)

ros=str(input("Jeżeli chcesz posortować tablicę rosnąco napisz 'r', jeżeli chcesz posortować tablicę malejąco napisz 'm'"))

if ros=="r":
    for i in range(0,(len(tab))): 
        m=0
        for i in range(0,(len(tab)-1)):
            if tab[m]>tab[m+1]:
                z=tab[m]
                tab[m]=tab[m+1]
                tab[m+1]=z
                m=m+1
            else:
                m=m+1
    print("Tablica posortowana rosnąco:", tab)


elif ros=="m":
    for i in range(0,(len(tab))):
        m=0
        for i in range(0,(len(tab)-1)):
            if tab[m]<tab[m+1]:
                z=tab[m]
                tab[m]=tab[m+1]
                tab[m+1]=z
                m=m+1
            else:
                m=m+1
    print("Tablica posortowana malejąco:", tab)