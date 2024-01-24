import random

def bomber(cntr,nbrs):

    def life(cell_value):
        if cell_value > 5:
            return 2
        elif cell_value == 5:
            return 1
        else:
            return 0
    
    living_true = life(nbrs.NW)//2 + life(nbrs.N)//2 + life(nbrs.NE)//2\
        + life(nbrs.W)//2 + life(nbrs.E)//2\
        + life(nbrs.SW)//2 + life(nbrs.S)//2 + life(nbrs.SE)//2

    if life(cntr) == 2:
        if living_true == 2 or living_true == 3:
            return 100
        elif living_true > 4 or living_true == 1:
            return 5
        elif life(nbrs.NW) == 1 or life(nbrs.N) == 1 or life(nbrs.NE) == 1 or\
        life(nbrs.W) == 1 or life(nbrs.E) == 1 or\
        life(nbrs.SW) == 1 or life(nbrs.S) == 1 or life(nbrs.SE) == 1:
            return 0
        else:
            return 100
    elif life(cntr) == 1:
        return 0
    else:
        if living_true == 5:
            return 100
        elif living_true == 0:
            return random.choice([0,0,0,0,0,0,0,0,100])
        else:
            return 0