def euclid(a,b):
    while a != b and b > 1 and a > 1:
        if a > b:
            a = a - b
        elif b > a:
            b = b - a
    if a == 1 or b == 1:
        return(False)
    else:
        return(True)