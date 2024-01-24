from math import sqrt

class Car:

    def __init__(self,mpg,ftc):
        self.currentFuel = ftc
        self.maxFuel = ftc
        self.mpg = mpg
        self.x = 0
        self.y = 0

    def driveTo(self,x,y):
        if sqrt((x-self.x)**2+(y-self.y)**2) <= (self.currentFuel)*(self.mpg):
            self.currentFuel = self.currentFuel - sqrt((x-self.x)**2+(y-self.y)**2)/self.mpg
            self.x = x
            self.y = y
            return True
        else:
            return False
    
    def getLocationX(self):
        return self.x
    
    def getLocationY(self):
        return self.y
    
    def getGas(self):
        return self.currentFuel
    
    def getToFill(self):
        return self.maxFuel - self.currentFuel