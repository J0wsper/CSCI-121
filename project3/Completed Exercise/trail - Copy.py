import random
from Body import Body
from geometry import Vector2D

class Trail1(Body):

    def __init__(self,bird):
        Body.__init__(self,bird.position,bird.velocity,bird.world)
        self.velocity = -bird.velocity + Vector2D(random.uniform(0.0,0.5),random.uniform(0.0,0.5))
        self.age = 0
        self.lifetime = 10

    def step(self):
        if self.age == self.lifetime:
            self.world.removeBody(self)
        self.age += 1

class Trail2(Body):

    def __init__(self,bird):
        Body.__init__(self,bird.position,bird.velocity,bird.world)
        self.velocity = -bird.velocity + Vector2D(random.uniform(0.0,0.5),random.uniform(0.0,0.5))
    
    def step(self):
        self.position += self.velocity
        self.velocity += self.accel
        if self.velocity.magnitude() < 0.01:
            self.world.removeBody(self)
        self.accel = self.steer()

    def steer(self):
        accel = (-0.5)*self.velocity
        return accel

    def color(self):
        while self.velocity.magnitude() > 0.1:
            if self.velocity.magnitude() > 0.4:
                return '#078e70'
            elif self.velocity.magnitude() > 0.2 and self.velocity.magnitude() < 0.4:
                return '#26ceaa'
            elif self.velocity.magnitude() > 0.08 and self.velocity.magnitude() < 0.2:
                return '#98e8c1'
            else:
                return '#f1eeff'