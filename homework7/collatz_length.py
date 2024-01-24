def collatz_length(n):
    if n <= 1:
        return 1
    if n > 1:
        if n%2 == 0:
            a = n//2
            return collatz_length(a)+1
        else:
            a = (n*3)+1
            return collatz_length(a)+1