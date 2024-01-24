def coins(c):
    cn = c//25+(c%25)//10+((c%25)%10)//5+c%5
    return cn