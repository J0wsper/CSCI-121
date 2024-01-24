def remainder(n,d):
    if n-d < 0:
        return n 
    else:
        a = n-d
        return remainder(a,d)