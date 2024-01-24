from Grid import Grid
from rules import *

Grid(age,
     '1. This is a function that judges the age of a cell. \
          it is born at an age the user chooses and slowly ages up \
            from the value to 100, then down to 0',
     pattern='patterns/rainbow_age.pat', generations=100)


Grid(decay,
     '2. This essentially just runs Conway except that dead cells\
        leave behind a decay trail that slowly decays from 100 to 0',
     pattern='patterns/good_smiley.pat', generations=200)


Grid(contrast,'3. This increases the contrast of an image.',
     pattern='images/reed-square.pgm',generations=3)


Grid(sharpen,'4. This sharpens the quality of an image.',
     pattern='images/reed-square.pgm',generations=4)

#I wanted to use a consistent image for this demo, so I used the reed square image again.


Grid(fill,'5. When presented with a closed white border,\
    this function will fill that area with color.',\
    pattern='patterns/fill.pat', generations=100)

#This is an arbitrary shape with a dash of color at its center. Any non-white color works for the fill, and any border works so long as it is closed.


Grid(shadow,'6. When presented with a white image, this function creates\
    a shadow of that image to the south-east.',\
    pattern='patterns/hi.pat',generations = 1)

#The shadow works with any shape so long as it is drawn in white. I chose hi because I thought it was funny.


Grid(exploding_maze,'7. This a function that creates a stable maze from scratch or from an input seed. The creation process is a bit chaotic.\
     The name is a holdover from what I was trying to make, but this ended up being significnatly more interesting.',\
    generations=30)

#The demonstration itself is a blank grid, but the exploding maze can be generated with a seed too. Either approach works.



Grid(war,'8. This is a simply simulation of a \'War\', where blue and red are fighting\
    for control of the board. The outcome, from what I have seen, is pseudo-random.')

#Again, this demo uses a blank state to start. You can pitch the battle one way or the other by introducing camps of red and blue at the outset, but\
#I liked the fact that the war could start from nothing.
