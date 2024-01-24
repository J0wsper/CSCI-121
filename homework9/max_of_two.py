def max_of_two(f,g,x):
    valueF = f(x)
    valueG = g(x)
    if valueF > valueG:
        return valueF
    else:
        return valueG