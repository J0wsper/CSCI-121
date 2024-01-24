def remove_duplicates(xs):
    index = 0
    while index < len(xs)-1:
        sindex = index + 1
        while sindex < len(xs):
            if xs[index] == xs[sindex]:
                del xs[sindex]
            else:
                sindex = sindex + 1
        index = index+1