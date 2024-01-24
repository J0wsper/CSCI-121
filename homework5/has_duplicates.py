def has_duplicates(xs):
    index = 0
    while index < len(xs)-1:
        sindex = index + 1
        while sindex < len(xs):
            if xs[index] == xs[sindex]:
                return(True)
            else:
                sindex = sindex + 1
        index = index + 1
    return(False)