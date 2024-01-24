def max_of_funcs(f,g):
    def h(a):
        if f(a) > g(a):
            return f(a)
        else:
            return g(a)
    return h