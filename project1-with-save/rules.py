import random

# * * * * * * * * * * * conway * * * * * * * * * * *
#
# Example of a grid rule. This rule gets applied to
# each grid cell, inspecting its state and the states
# of its eight neighbor cells, and is used to determine
# its next state.
#
# This particular rule encodes the behavior of Conway's 
# game of life simulation.  It takes two parameters:
#
#   cntr: the state of the grid cell being inspected
#
#   nbrs: collection of states of the 8 grid neighbors 
#         that sit around the cell being inspected
#
# This rule interprets states of 0 as "dead" and
# states of 1 and above as being "alive". 
#
# Live cells die if they have too many or too many
# living neighbors.
#
# Dead cells come alive if they have just the 
# right number of live neighbors.
#
# See the if/else below for details.
#
def conway(cntr,nbrs):

    # live
    #
    # Helper function that returns 1/0 if live/dead.
    def life(cell_value):
        if cell_value > 0:
            return 1
        else:
            return 0

    #
    # count the number of living neighbors  
    #
    living = life(nbrs.NW) + life(nbrs.N) + life(nbrs.NE) \
           + life(nbrs.W) + life(nbrs.E) \
           + life(nbrs.SW) + life(nbrs.S) + life(nbrs.SE)

    #
    # determine next state
    #
    # if alive...
    if life(cntr) == 1:
        # and there are two or three live neighbors...
        if living == 2 or living == 3:
            # survive
            return cntr
        else:
            # otherwise, die.
            return 0
    #
    # if dead...
    else:
        # but there are three live neighbors...
        if living == 3:
            # come alive.
            return 100
        else:
            return 0
#
#
# * * * * * * * * * * * conway * * * * * * * * * * *



# * * * * * * * * * generational * * * * * * * * * * *
#
# This performs Conway's game of life except, when a
# cell is alive (1-100), its value is interpreted as
# its "generation".  This means that, when a live cell
# is born, it takes on the value that's one more than 
# the max value of its live neighbors.
#
def generational(cntr,nbrs):

    # live
    #
    # Helper function that returns 1/0 if live/dead.
    def life(cell_value):
        if cell_value > 0:
            return 1
        else:
            return 0

    #
    # count the number of living neighbors  
    #
    living = life(nbrs.NW) + life(nbrs.N) + life(nbrs.NE) \
           + life(nbrs.W) + life(nbrs.E) \
           + life(nbrs.SW) + life(nbrs.S) + life(nbrs.SE)

    largest = max(nbrs.NW,nbrs.N,nbrs.NE,nbrs.W,
                  nbrs.SE,nbrs.S,nbrs.SW,nbrs.E)
    #
    # determine next state
    #
    # if alive...
    if life(cntr) == 1:
        # and there are two or three live neighbors...
        if living == 2 or living == 3:
            # survive
            return cntr
        else:
            # otherwise, die.
            return 0
    #
    # if dead...
    else:
        # but there are three live neighbors...
        if living == 3:
            # come alive, marking your new generation
            return 1+largest
        else:
            return 0
#
#
# * * * * * * * * * generational * * * * * * * * * * *

# * * * * * * * * * * * blur * * * * * * * * * * * * * 
#
# Example of an image processing rule.  This blurs an
# image.  A cell becomes the average of itself with
# the average value of its neighbors.  This "blends"
# greys and "smooths" out sharp transitions.  The 
# effect of a bright pixel is spread over an area
# of the image, centered at that pixel.

def blur(cntr,nbrs):

    # compute the average value of my neighbors
    avg = (nbrs.N + nbrs.E + nbrs.S + nbrs.W)//4

    # change state so that I'm closer to their average
    return (cntr + avg) // 2

#
#              
# * * * * * * * * * * * blur * * * * * * * * * * * * * 

# * * * * * * * * * * negative * * * * * * * * * * * * 
#
# This inverts brightness to darkness, and vice versa,
# in an image.  The effect makes the image look like 
# a photographic negative.
#
def negative(cntr,nbrs):
    return 255 - cntr
#
#
# * * * * * * * * * * negative * * * * * * * * * * * * 

# * Age *

def life(cell_value):
        if cell_value > 0:
            return 1
        else:
            return 0

def age(cntr,nbrs):
    # if the cell is at the end of its life, die
    if cntr == 100:
        return 0
    #if the cell isn't about to die or dead, increment the age
    elif life(cntr) == 1:
        return cntr+1
    else:
        #otherwise, stay dead
        return 0

# * Age End *    

# * Decay *

def decay(cntr,nbrs):

    # live
    #
    # Helper function that returns 1/0 if live/dead.
    def life(cell_value):
        if cell_value == 100:
            return 1
        else:
            return 0

    #
    # count the number of living neighbors  
    #
    living = life(nbrs.NW) + life(nbrs.N) + life(nbrs.NE) \
           + life(nbrs.W) + life(nbrs.E) \
           + life(nbrs.SW) + life(nbrs.S) + life(nbrs.SE)

    #
    # determine next state
    #
    # if alive...
    if life(cntr) == 1:
        # and there are two or three live neighbors...
        if living == 2 or living == 3:
            # survive
            return cntr
        # otherwise   
        else:
            # die by turning into a new color
            return cntr-1
    #
    # if dead...
    else:
        # but there are three live neighbors...
        if living == 3:
            # come alive.
            return 100
        #if dead and not quite fully dead
        elif life(cntr) == 0 and cntr != 0:
            # die more
            return cntr-1
        #otherwise, stay dead
        else:
            return 0

# * Decay *

# * Contrast *

#basically a simple if statement checking if a cell is above or below the middle grey value. If it is above, increase the value. If it is below, decrease.
def contrast(cntr,nbrs):
    if cntr > 127:
        return cntr+10
    elif cntr < 127:
        return cntr-10
    else:
        return cntr

# * Contrast End *

# * Sharpen *

def sharpen(cntr,nbrs):
    #average value
    avg = (nbrs.E + nbrs.S + nbrs.W + nbrs.N)//4
    #add the half the difference between the cntr and the average to the center
    return cntr + (cntr-avg)//2

# * Sharpen End *

# * Fill *

def fill(cntr,nbrs):
    
    #checks whether or not a cell is a boundary cell
    def is_boundary(cell_value):
        if cell_value == 100:
            return 1
        else:
            return 0

    #checks whether or not a cell is a color cell
    def is_color(cell_value):
        if cell_value == 100:
            return 0
        elif 0 < cell_value < 100:
            return 1
        else:
            return 0
    
    #checks the amount of colored cells
    presence = is_color(nbrs.NW) + is_color(nbrs.N) + is_color(nbrs.NE)\
        + is_color(nbrs.E) + is_color(nbrs.W)\
        + is_color(nbrs.SW) + is_color(nbrs.S) + is_color(nbrs.SW)
    
    #creates a list of neighbors
    neighbors_list = [nbrs.NW,nbrs.N,nbrs.NE,nbrs.W,nbrs.E,nbrs.SW,nbrs.S,nbrs.SE]

    #if you're a boundary cell, stay that way
    if is_boundary(cntr) == 1:
        return cntr
    #if you're not and you're near color, become that color
    elif presence >= 1 and is_boundary(cntr) == 0:
        for i in neighbors_list:
            if is_color(i) == 1:
                return i
    else:
        return 0

# * Fill End *

# * Shadow *

def shadow(cntr,nbrs):
    
    def life(cell_value):
        if cell_value == 100:
            return 1
        else:
            return 0

    #maintaining the neighbors
    if life(cntr) == 1:
        return cntr
    #drawing the shadow
    elif life(cntr) != 1 and life(nbrs.NW) == 1:
        return 50
    #dying otherwise
    else:
        return 0

# * Shadow End *

# * Exploding Maze *

def exploding_maze(cntr,nbrs):

    #the same helper function we've been using for a while
    def life(cell_value):
        if cell_value > 5:
            return 2
        elif cell_value == 5:
            return 1
        else:
            return 0
    
    #judges the amount of truly alive neigbors, i.e the ones that aren't red (the 'bombers') or completely dead.
    living_true = life(nbrs.NW)//2 + life(nbrs.N)//2 + life(nbrs.NE)//2\
        + life(nbrs.W)//2 + life(nbrs.E)//2\
        + life(nbrs.SW)//2 + life(nbrs.S)//2 + life(nbrs.SE)//2

    #if you are alive:
    if life(cntr) == 2:
        #stay alive if you have a suitable amount of living neighbors
        if living_true == 2 or living_true == 3:
            return 100
        #if you have too many or too few living neighbors, turn into a red bomber
        elif living_true > 4 or living_true == 1:
            return 5
        #if any of your neighbors is a bomber, die
        elif life(nbrs.NW) == 1 or life(nbrs.N) == 1 or life(nbrs.NE) == 1 or\
        life(nbrs.W) == 1 or life(nbrs.E) == 1 or\
        life(nbrs.SW) == 1 or life(nbrs.S) == 1 or life(nbrs.SE) == 1:
            return 0
        #otherwise, remain alive
        else:
            return 100
    #if you are a bomber, die
    elif life(cntr) == 1:
        return 0
    #if you are dead
    else:
        #if you have enough 2 living neighbors, come back to life (this value can be changed to do different things. For example, 3 makes the\
        # system too chaotic to stabilize, 4 and up makes the system sparse and turns the grid into a 'minefield')
        if living_true == 2:
            return 100
        #otherwise, if everything is dead, randomly choose a value
        elif living_true == 0:
            return random.choice([0,0,0,0,0,0,0,0,100])
        else:
            return 0

# * Exploding Maze End *

# * War *

def war(cntr,nbrs):

    #a modified life helper function. Different colors get different life assignments.
    def life(cell_value):
        if cell_value == 100:
            return 3
        if cell_value == 80:
            return 2
        if cell_value == 5:
            return 1
        else:
            return 0

    #counting the amount of living blue neighbors with integer manipulation
    living_blue = life(nbrs.NW)%3//2 + life(nbrs.N)%3//2 + life(nbrs.NE)%3//2 \
           + life(nbrs.W)%3//2 + life(nbrs.E)%3//2 \
           + life(nbrs.SW)%3//2 + life(nbrs.S)%3//2 + life(nbrs.SE)%3//2

    #same thing with red neighbors
    living_red = (life(nbrs.NW)%3)%2 + (life(nbrs.N)%3)%2 + (life(nbrs.NE)%3)%2 \
           + (life(nbrs.W)%3)%2 + (life(nbrs.E)%3)%2 \
           + (life(nbrs.SW)%3)%2 + (life(nbrs.S)%3)%2 + (life(nbrs.SE)%3)%2

    #if you're not red or blue, randomly choose a side
    if life(cntr) != 1 and life(cntr) != 2:
        return random.choice([0,5,80])
    else:
        #if you have 3 red and 3 blue neighbors, randomly choose your side
        if living_blue == 3 and living_red == 3:
            return random.choice([5,80])
        #if you only have 3 blue neihgbors, turn blue
        elif living_blue == 3:
            return 80
        #same for red
        elif living_red == 3:
            return 5
        #otherwise, if the blues outnumber the reds, turn blue
        elif living_blue > living_red:
            return 80
        #same for red
        elif living_blue < living_red:
            return 5
        #otherwise, remain dead
        else:
            return 0