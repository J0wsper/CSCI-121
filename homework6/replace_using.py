def replace_using(s,d):
    ls = s.split(' ')
    index = 0
    while index < len(ls):
        if ls[index] in d:
            ls[index] = d[ls[index]]
        index = index + 1
    a = ' '.join(ls)
    return a