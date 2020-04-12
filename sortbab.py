def sortbabe(x):
    
    for t in range(len(x)-1):
        for y in range(len(x)-1):
            if x[y]>x[y+1]:
                z=x[y]
                x[y]=x[y+1]
                x[y+1]=z
    return x