def bubble_sort(to_sort):
    done=False
    while not done:
        same=0
        for i in range(len(to_sort)-1):
            if to_sort[i]>to_sort[i+1]:
                x=to_sort[i]
                to_sort[i]=to_sort[i+1]
                to_sort[i+1]=x
            else:
                same+=1
        if same==len(to_sort)-1:
            done = True
    return to_sort
