def counts(n,xs):
    a = 0
    s = [0]*n
    while a < len(xs):
        s[xs[a]] = s[xs[a]]+1
        a = a + 1
    return(s)
