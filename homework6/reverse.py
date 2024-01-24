def inverse(d):
    entries = []
    for i in d:
        entries.append(d[i])
    keys = []
    for i in d:
        keys.append(i)
    a = {}
    index = 0
    while index < len(keys):
        if entries[index] in a:
            a[entries[index]] = a[entries[index]] + [keys[index]]
        else:
            a[entries[index]] = [keys[index]]
        index = index + 1
    return a