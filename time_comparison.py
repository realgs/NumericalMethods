from bubble_sort import bubble_sort
from selection_sort import selection_sort
from merge_sort import merge_sort
from insertion_sort import insertion_sort

import timeit
import random

to_time=[]
for _ in range(500):
    to_time.append(random.randint(0,10000))
to_time_2= to_time[:]
to_time_3= to_time[:]
to_time_4= to_time[:]

def f():
    return bubble_sort(to_time)
print('Bubble sort: ',timeit.timeit(f,number=100)/100)
def f():
    return selection_sort(to_time_2)
print('Selection sort: ',timeit.timeit(f,number=100)/100)
def f():
    return merge_sort(to_time_3)
print('Merge sort: ',timeit.timeit(f,number=100)/100)
def f():
    return insertion_sort(to_time_4)
print('Insertion sort: ',timeit.timeit(f,number=100)/100)