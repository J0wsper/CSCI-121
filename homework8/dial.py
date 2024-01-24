class Dial:

    def __init__(self,lim,on,off):
        self.amountOn = 0
        self.max = lim
        self.off = off
        self.on = on
    
    def display(self):
        print('['+str(self.on*(self.amountOn)+self.off*(self.max-self.amountOn))+']')
    
    def increaseBy(self,turnUp):
        if turnUp >= self.max or self.amountOn == self.max or (turnUp > self.max - self.amountOn):
            self.amountOn = self.max
        else:
            self.amountOn += turnUp

    def decreaseBy(self,turnDown):
        if turnDown >= self.max or turnDown > self.amountOn:
            self.amountOn = 0
        else:
            self.amountOn -= turnDown
