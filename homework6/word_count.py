def word_count(s):
    ls = s.split(' ')
    d = {}
    index = 0
    while index < len(ls):
        if ls[index] not in d:
            d[str(ls[index])] = 1
        elif ls[index] in d:
            d[str(ls[index])] = d[str(ls[index])]+1
        index = index + 1
    return d