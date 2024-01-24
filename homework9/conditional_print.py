def conditional_print(test):
    def condprint(a):
        if test(a) == True:
            print(a)
    return condprint