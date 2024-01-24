def prime_finder(p):
    b = 2
    while b < p:
        if p%b == 0:
            return(False)
        else:
            b = b + 1
    return(True)

def primes_list(n):
    prime = []
    a = 2
    index = 0
    while len(prime) < n:
        if prime_finder(a) == True:
            prime.append(a)
            index = index+1
        a = a + 1
    return(prime)