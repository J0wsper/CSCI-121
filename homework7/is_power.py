def is_power(n,b):
    if n == 1:
        return True
    else:
        if n%b == 0:
            a = n//b
            return is_power(a,b)
        else:
            return False