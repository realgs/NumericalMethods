def insertion_sort(to_sort):
    for i in range(len(to_sort)-1):
        x=i
        while to_sort[x+1]<to_sort[x] and x>=0:
            to_sort[x]-=to_sort[x+1]#change position
            to_sort[x+1]+=to_sort[x]
            to_sort[x]=to_sort[x+1]-to_sort[x]
            x-=1
    return to_sort