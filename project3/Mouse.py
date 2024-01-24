from Body import Body
from geometry import Vector2D

class Mouse(Body):

    def __init__(self,world):
        p0 = 0
        v0 = 0
        Body.__init__(self,v0,p0,world)

    def step(self):
        self.position = self.world.pointer()
    
    def color(self):
        return '#00ff00'
