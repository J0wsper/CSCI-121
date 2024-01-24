def reverse_number(n):
    a = 0
    b = 0
    while n//(10**a) > 0:
        b = b*10 
        b = b + (n%(10**(a+1)))//(10**a)
        a = a + 1
    return(b)

def count_palindromes(m):
    a = 0
    s = 0
    while a <= m:
        if a == reverse_number(a):
            s = s + 1
        a = a + 1
    return(s)