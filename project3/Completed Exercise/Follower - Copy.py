from Bird import Bird
from geometry import Vector2D

class Follower(Bird):
    
    COHERE_COEFF = 7.0
    COHERE_RADIUS = 20.0

    def computeCohere(self):
        
        nearby = self.flock.allWithinDistance(self.COHERE_RADIUS,self.position,excluding=[self])

        cohere = Vector2D()
        if self.flock.leader in nearby:
            cohere += self.flock.leader.position - self.position
            return cohere.direction()
        else:
            return Vector2D()