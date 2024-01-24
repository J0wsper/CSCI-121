def make_even(xs):
    index = 0
    while index < len(xs):
        if xs[index]%2 == 1:
            xs[index] = xs[index]-1
        else:
            xs[index] = xs[index]
        index = index+1
