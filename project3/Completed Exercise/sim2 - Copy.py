import time
from World import World
from Flock import Flock
from Bird import Bird

#
# CSCI 121: Flocks
# Project 3 Option #2 Exercise 1
#
# This script runs the simulation for EXERCISE 1.
#

# Initialize the world and its window.
world = World(60.0,45.0,600,450,topology='wrapped')
flock = Flock(Bird,10,world)
world.addSystem(flock)

# Turn on the flock's trails. 
for bird in flock:
    bird.setTrail(3)

# Run the simulation indefinitely.
while True:
    time.sleep(0.01)
    world.step()
    world.render()
