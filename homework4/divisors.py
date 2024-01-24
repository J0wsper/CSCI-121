def divisors(n):
    a = 1
    divisors_string = ''
    if n == 1:
        return('The divisor of 1 is 1.')
    else:
        while a <= n:
            if n%a == 0 and n == a:
                divisors_string = divisors_string+'and '+str(a)
            elif n%a == 0 and n!= a:
                divisors_string = divisors_string+str(a)+', '
            a = a+1
        if divisors_string == '1, and '+str(n):
            return('The divisors of '+str(n)+' are 1 and '+str(n)+'.')
        else:
            return('The divisors of '+str(n)+' are '+divisors_string+'.')