def nd(number):
    if 10 < number < 20:
        return(str(number)+'th')
    else:
        if number%10 == 3:
            return(str(number)+'rd')
        elif number%10 == 2:
            return(str(number)+'nd')
        elif number%10 == 1:
            return(str(number)+'st')
        else:
            return(str(number)+'th')