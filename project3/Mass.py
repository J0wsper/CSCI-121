from Body import Body
from geometry import Vector2D, Point2D

class Mass(Body):

    ATTRACT_RADIUS = 200.0

    MAXIMUM_SPEED = 100.0
    
    def __init__(self, p0, v0, world, flock, mass):
        Body.__init__(self, p0, v0, world)
        self.flock = flock
        self.mass = mass
    
    def steer(self):

        nearby = self.flock.allWithinDistance(self.ATTRACT_RADIUS, self.position, excluding=[self])
        
        offset = Vector2D()
        for other in nearby:
            offset = other.position - self.position
            distance = offset.magnitude()
            weight = (other.mass*self.mass)/(distance**2)
        return offset * weight