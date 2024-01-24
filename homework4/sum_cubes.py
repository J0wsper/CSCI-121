from cmath import sqrt


def sum_cubes(n):
    a = 1
    sum = 0
    while a <= n:
        sum = sum+a**3
        a = a+1
    return(sum)