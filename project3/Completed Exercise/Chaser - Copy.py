from Bird import Bird
from geometry import Vector2D

class Chaser(Bird):

    def computeCohere(self):
        mousePosition = self.world.pointer()
        cohere = Vector2D()
        offset = mousePosition - self.position
        cohere += offset
        return cohere.direction()

