import time
from World import World
from Flock_Mass import Flock_Mass
from Mass import Mass
from geometry import Point2D, Vector2D
from random import *

#
# CSCI 121: Flocks
# Project 3 Option #2 Exercise 6
#
# This script runs the simulation for EXERCISE 6.
#


# Initialize the world and its window.
world = World(60.0,45.0,800,600,topology='wrapped')
flock = Flock_Mass(Mass,4,world)
for i in range(5):
    h = Mass(Point2D.random(world.bounds),Vector2D(0.0,1.0),flock,world,randrange(1,50))
    flock.add(h)
world.addSystem(flock)

# Run the simulation indefinitely.
while True:
    time.sleep(0.01)
    world.step()
    world.render()
