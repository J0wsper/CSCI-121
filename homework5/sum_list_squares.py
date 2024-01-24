def sum_list_squares(n):
    a = 0
    s = 0
    while a < len(n):
        s = s + (n[a])**2
        a = a + 1
    return(s)