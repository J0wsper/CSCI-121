def average(f,start,end):
    index = start
    fSum = 0
    while index <= end:
        fSum += f(index)
        index += 1
    fAvg = fSum/((end+1)-start)
    return fAvg