from Bird import Bird
from geometry import Vector2D, Point2D
from Flock import Flock
from random import *

class Herder(Bird):

    HERD_RADIUS = 20.0

    MAXIMUM_SPEED = 1.0

    rightmost = None

    def steer(self):
        
        rightmost = None

        nearby = self.flock.allWithinDistance(self.HERD_RADIUS, self.position, excluding=[self])

        offset = Vector2D()
        for bird in nearby:
            if rightmost is None:
                    rightmost = bird
                    offset += (self.velocity - rightmost.velocity)
                    #print('What')
            else:
                if (self.velocity).dot(bird.position - self.position) > 0.0:    
                    #print((bird.position - self.position).cross(rightmost.position - self.position))
                    if (bird.position - self.position).cross(rightmost.position - self.position) > 0.0:
                        rightmost = bird
                        offset += (self.position - rightmost.position)
        if rightmost is None:
            return Vector2D()
        else:
            return offset.direction()

    def color(self):
        return '#0000ff'

