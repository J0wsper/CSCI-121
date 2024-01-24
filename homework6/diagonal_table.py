def diagonal_table(s):
    xs = []
    index = 0
    while index < s:
        ys = []
        sindex = 0
        while sindex < s:
            if index == sindex:
                ys.append(1)
            else:
                ys.append(0)
            sindex = sindex+1
        xs.append(ys)
        index = index + 1
    return(xs)
