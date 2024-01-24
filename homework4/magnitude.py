def magnitude(n):
    a = 0
    while 2**a<=n:
        a = a + 1
    return(a)