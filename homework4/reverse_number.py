def reverse_number(n):
    a = 0
    b = 0
    while n//(10**a) > 0:
        b = b*10 
        b = b + (n%(10**(a+1)))//(10**a)
        a = a + 1
    return(b)
#have an iterative digit a
#take the modulus of the input divided by 10^a = b
#that gives the first digit
#add 1 to the iterative digit
#multiply b by ten to make room for the next digit