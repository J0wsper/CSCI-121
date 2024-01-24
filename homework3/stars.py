def stars(width,height):
    s = ('* '*(width//2)+'*'*(width%2)+'\n'+' *'*(width//2)+' '*(width%2)+'\n')*(height//2)+('* '*(width//2)+'*'*(width%2)+'\n')*(height%2)
    return(s)
