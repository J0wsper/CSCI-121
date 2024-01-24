def quotient(n,d):
    if n - d >= 0:
        r = n-d
        return quotient(r,d)+1
    else:
        return 0