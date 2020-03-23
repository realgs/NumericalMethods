import random as ran
import time
print("Podaj z jakiego zakresu losujemy elementy do tabeli.")
x=int(input("Losujemy od: "))
y=int(input("Losujemy do: "))
tab=[]

for i in range(0,ran.randint(0,40)):
    tab.append(ran.randint(x,y))
print("Nasza tablica:",tab)

ros=str(input("Jeżeli chcesz posortować tablicę rosnąco napisz 'r', jeżeli chcesz posortować tablicę malejąco napisz 'm'"))
start = time.clock()
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
    end=time.clock()
    total1=end-start
    print("Tablica posortowana rosnąco:", tab)
    print("{0:02f}s".format(total1))

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
        end=time.clock()
    total2=end-start
    print("Tablica posortowana malejąco:", tab)
    print("{0:02f}s".format(total2))




lista=[1,2,5,6,89,10,22,1,30,100,2]
start=time.clock()
lista.sort()
end= time.clock()
total3=end-start
print(lista)
print("{0:02f}s".format(total3))

data = [6,-1,8,10,4,50,2,0,100,34,2,3,4]
start=time.clock()
def bubb_sort(data):
    for i in range(len(data) - 1, 0, -1):
        for j in range(i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]

bubb_sort(data)
end= time.clock()
total4=end-start
print(data)
print("{0:02f}s".format(total4))