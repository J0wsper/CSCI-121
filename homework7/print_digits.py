def print_digits(n):
    a = n%10
    print(a)
    if n//10 > 0:
        return print_digits(n//10)