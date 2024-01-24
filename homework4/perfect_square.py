def perfect_square(n):
    a = 0
    while a**2 < n:
        a = a+1
    if a**2 == n:
        return(True)
    else:
        return(False)