def down_up(n):
    a = []
    b = n
    while n > 0:
        a = a+[n]
        n = n-1
    n = 2
    while n <= b:
        a = a+[n]
        n = n+1
    return(a)