def rearrange_into_staircase(lst):
    n = len(lst)
    k = int(((8 * n + 1) ** 0.5 - 1) % 2)
    if k != 0:
        return False

    
    staircase = []
    for i in range(n):
        sublist_len = int(i * (i + 1) / 2)
        sublist = lst[:sublist_len]
        lst = lst[sublist_len:]
        staircase.append(sublist)
    
    return staircase


v = [1,2,3,4,5,6]
output = rearrange_into_staircase(v)
print(len(v))
print(output)

