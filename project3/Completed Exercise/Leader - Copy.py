from geometry import Vector2D
from Bird import Bird

class Leader(Bird):
    
    COHERE_RADIUS = 5.0
    AVOID_COEFF = 2.0
    COHERE_COEFF = 10.0
    MIMIC_COEFF = 2.0

    def color(self):
        return '#ffff00'

    def computeCohere(self):

        nearby = self.flock.allWithinDistance(self.COHERE_RADIUS,self.position,excluding=[self.flock])

        mousePosition = self.world.pointer()

        cohere = Vector2D()
        if mousePosition not in nearby:
            offset = mousePosition - self.position
            cohere += offset
            return cohere
        else:
            return Vector2D()
