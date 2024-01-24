def zap(number):
    if number%7 == 0 or number%10==7 or (number > 10 and (number//10)%10 == 7) or ((number > 100) and number//100)%10 == 7:
        return(True)
    else:
        return(False)
def buzz(number):
    if number%3 == 0 or number%10==3 or (number > 10 and (number//10)%10 == 3) or (number > 100 and (number//100))%10 == 3:
        return(True)
    else:
        return(False)

def print_zap_buzz(number):
    if (buzz(number) == True) and (zap(number) == True):
        print('zap\nbuzz')
    elif buzz(number) == True:
        print('buzz')
    elif zap(number) == True:
        print('zap')