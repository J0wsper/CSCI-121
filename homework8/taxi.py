from math import sqrt

class Car:

    def __init__(self,mpg,ftc):
        self.currentFuel = ftc
        self.maxFuel = ftc
        self.mpg = mpg
        self.x = 0
        self.y = 0
        self.tally = 0
        self.passenger = False

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

class Taxi(Car):

    def pickup(self):
        if self.passenger == True:
            return False
        else:
            self.tally += 2
            self.passenger = True
            return True
        
    def dropoff(self):
        if self.passenger == True:
            self.passenger = False
            return True
        else:
            return False

    def getMoney(self):
        return self.tally

    def driveTo(self,x,y):
        if sqrt((x-self.x)**2+(y-self.y)**2) <= (self.currentFuel)*(self.mpg):
            self.currentFuel = self.currentFuel - sqrt((x-self.x)**2+(y-self.y)**2)/self.mpg
            if self.passenger == True:
                self.tally += 3*sqrt((x-self.x)**2+(y-self.y)**2)
            self.x = x
            self.y = y
            return True
        else:
            return False