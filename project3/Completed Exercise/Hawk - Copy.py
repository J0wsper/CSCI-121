from Bird import Bird
from Body import Body
from geometry import Vector2D
from geometry import Point2D

class Hawk(Bird):

    MAXIMUM_SPEED = 1.5
    COHERE_RADIUS = 30.0
    AVOID_COEFF = 0.0
    MIMIC_COEFF = 0.0

    def __init__(self,p0,v0,flock,world):
        Bird.__init__(self,p0,v0,flock,world)
        self.position0 = p0
        self.velocity0 = v0
        self.world = world
        self.flock = flock

    def computeCohere(self):

        target = Vector2D(0.0,0.0)
        for i in self.flock:
            offset = i.position - self.position
            target += offset
        target = target*(1/target.magnitude())

        if target.magnitude() < 20.0:
            return target
        else:
            return Vector2D()

    def color(self):
        return '#ff0000'