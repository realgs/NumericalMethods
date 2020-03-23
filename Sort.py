import random as ran
print("Podaj z jakiego zakresu losujemy elementy do tabeli.")
x=int(input("Losujemy od: "))
y=int(input("Losujemy do: "))
tab=[]

for i in range(0,ran.randint(0,40)):
    tab.append(ran.randint(x,y))
print("Nasza tablica:",tab)

ros=str(input("Jeżeli chcesz posortować tablicę rosnąco napisz 'r', jeżeli chcesz posortować tablicę malejąco napisz 'm'"))
