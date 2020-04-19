def dividing(to_sort):
    return to_sort[:len(to_sort)//2],to_sort[len(to_sort)//2:]

def merge(left,right):
    if len(left)==0:
        return right
    elif len(right)==0:
        return left

    merged=[]
    left_index=0
    right_index=0
    while len(merged)<(len(left)+len(right)):
        if left[left_index]<=right[right_index]:
            merged.append(left[left_index])
            left_index+=1
        else:
            merged.append(right[right_index])
            right_index+=1
        if len(left)==left_index:
            merged+=right[right_index:]
            break
        if len(right)==right_index:
            merged+=left[left_index:]
            break
    return merged

def merge_sort(to_sort):
    if len(to_sort) <=1:
        return to_sort
    else:
        l,r=dividing(to_sort)
        return merge(merge_sort(l),merge_sort(r))
