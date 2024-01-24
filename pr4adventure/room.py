import random
from monster import *
from math import ceil, floor

def weightedRandom(dct):
    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        total += v
        if rand_val <= total:
            return k
    assert False, 'unreachable'

class Room:

    def __init__(self, description):
        self.desc = description
        self.dif = 0
        self.monsters = []
        self.exits = []
        self.items = []
        self.lootTable = {}
        self.soldItems = {}
        self.spawnTable = {}
        self.firstEntry = True

    def addExit(self, exitName, destination):
        self.exits.append([exitName, destination])

    def getDestination(self, direction):
        for e in self.exits:
            if e[0] == direction:
                return e[1]

    def connectRooms(room1, dir1, room2, dir2):
        #creates "dir1" exit from room1 to room2 and vice versa
        room1.addExit(dir1, room2)
        room2.addExit(dir2, room1)

    def exitNames(self):
        return [x[0] for x in self.exits]

    def addItem(self, item):
        self.items.append(item)

    def removeItem(self, item):
        self.items.remove(item)

    def addMonster(self, monster):
        self.monsters.append(monster)

    def removeMonster(self, monster):
        self.monsters.remove(monster)

    def hasItems(self):
        return self.items != []

    def getItemByName(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False

    def hasMonsters(self):
        return self.monsters != []

    def getMonsterByName(self, name):
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
        return False

    def randomNeighbor(self):
        return random.choice(self.exits)[1]

    def updateDif(self,newDif):
        self.dif = newDif

    def getDif(self):
        return self.dif
        
    def handleFirstEntry(self):

        #Creating the spawn table depending on the difficulty of the room.
        if self.dif <= 3:
            self.spawnTable = {Mole(self): 0.33, Scrap(self): 0.33, Warlock(self): 0.34}
            self.lootTable = {gShard(): 0.25, dShard(): 0.25, sShard(): 0.25, Claymore(): 0.08, Knife(): 0.08, Scimitar(): 0.09}
            self.soldItems = {Claymore(): 0.15, Knife(): 0.15, Scimitar(): 0.15, CRobes(): 0.10, Leather(): 0.10, Ration(): 0.25, BluePotion(): 0.1}

        elif self.dif <= 6 and self.dif > 3:
            self.spawnTable = {Mole(self): 0.10, Scrap(self): 0.10, Warlock(self): 0.10,\
                 Traitor(self): 0.23, Knight(self): 0.24, Shadow(self): 0.23}
            self.lootTable = {gShard(): 0.2, dShard(): 0.2, sShard(): 0.2, Claymore(): 0.1, Knife(): 0.1, Scimitar(): 0.1,\
                GreatSword(): 0.033, Flail(): 0.033, Cleaver(): 0.034}
            self.soldItems = {Claymore(): 0.05, Knife(): 0.05, Scimitar(): 0.05, CRobes(): 0.05, Leather(): 0.05, \
                Ration(): 0.2, BluePotion(): 0.1, WRobes(): 0.1, Plate(): 0.1, GreatSword(): 0.08, Flail(): 0.08, Cleaver(): 0.09} 

        else:
            self.spawnTable = {Traitor(self): 0.10, Knight(self): 0.10, Shadow(self): 0.10,\
                 Warlord(self): 0.24, Orogene(self): 0.23, Omen(self): 0.23}
            self.lootTable = {gShard(): 0.2, dShard(): 0.2, sShard(): 0.2, Claymore(): 0.05, Knife(): 0.05, Scimitar(): 0.05,\
                GreatSword(): 0.07, Flail(): 0.06, Cleaver(): 0.07, Woe(): 0.016, Plague(): 0.016, Flayer(): 0.018}
            self.soldItems = {GreatSword(): 0.1, Flail(): 0.1, Cleaver(): 0.1, WRobes(): 0.1, Plate(): 0.1,\
                Ration(): 0.2, BluePotion(): 0.1, Plague(): 0.07, Woe(): 0.07, Flayer(): 0.06} 

        self.firstEntry = False
        self.index = 0

        #Add monsters
        while self.index < ceil(self.dif/3):
            self.addMonster(weightedRandom(self.spawnTable))
            self.index += 1
       
        for i in self.monsters:
            lootQuantity = random.randrange(1,2*self.dif)
            index = 0
            while index < lootQuantity:
                i.loot.append(weightedRandom(self.lootTable))
                index += 1
            soldQuantity = random.randrange(1, 2*self.dif)
            index = 0
            while index < soldQuantity:
                i.soldItems.append(weightedRandom(self.soldItems))
                index += 1

        #Also, spawn chests
        self.spawnChest()

    def spawnChest(self):
        if random.random() < 0.2:
            if self.dif <= 3:
                activeChest = Chest('Wooden chest', 'A simple wooden chest', [], False)
                self.items.append(activeChest)
                activeChest.contents.append(weightedRandom(self.lootTable))
                activeChest.contents.append(weightedRandom(self.lootTable))
            elif self.dif <= 5 and self.dif > 3:
                activeChest = Chest('Lockbox', 'A rusted lockbox', [], False)
                self.items.append(activeChest)
                activeChest.contents.append(weightedRandom(self.lootTable))
                activeChest.contents.append(weightedRandom(self.lootTable))
                activeChest.contents.append(weightedRandom(self.lootTable))
            elif self.dif <= 7 and self.dif > 5:
                activeChest = Chest('Steel Chest', 'A steel chest', [], False)
                self.items.append(activeChest)
                activeChest.contents.append(weightedRandom(self.lootTable))
                activeChest.contents.append(weightedRandom(self.lootTable))
                activeChest.contents.append(weightedRandom(self.lootTable))
                activeChest.contents.append(weightedRandom(self.lootTable))


class mDelta(Room):
    """
    The mycelium delta. A room full of mushrooms and fungi, with a miasma of spores obscuring your vision. 
    You can feel a shortness in your breath the longer you stay in here.
    """
    #The mycelium delta does chip damage to the player whenever they enter or if they decide to stay there.
    def handleEntry(self,player):
        if self.firstEntry == True:
            self.handleFirstEntry()
        else:
            player.health -= ceil(1/16)*player.maxHealth

class uRiver(Room):
    """
    The underground river. Villages dot the area, all harvesting their bounty from the river's generosity.
    The river air heals you, but you sense that you will find more monsters in this area.
    """
    def __init__(self,description,typing):
        Room.__init__(self,description)
        self.typing = typing

    #The underground river spawns more monsters than most other locales. Depending on the type, the villagers will either be
    #friendly or hostile.

    def handleEntry(self,player):
        
        #Creating the spawn table depending on the difficulty of the room.

        #If this is the player's first entry:
        if self.firstEntry is True:
            self.handleFirstEntry()


        else:
            self.firstEntry = False
            if player.health < 1//2*player.maxHealth:
                player.health += ceil(1/16)*player.maxHealth
            if random.random() > 0.7 and len(self.monsters) < 3:
                Riverfolk(self,self.typing)
        

class sWaste(Room):
    """
    The salt wastes. You don't see any monsters here, probably because they hate the inhospitable soil.
    You think this is a safe place to rest. 
    """
    #The salt wastes don't do anything when the player enters them.
    def handleEntry(self,player):
        if self.firstEntry == True:
            self.handleFirstEntry()
        else:
            if random.random() > 0.95:
                if random.random() > 0.95:
                    player.health -= floor(1/2)*player.maxHealth
                    print('A stalagmite has fallen on you! It landed on a critical location, dealing massive damage.')
                    print()
                else:
                    player.health -= floor(1/8)*player.maxHealth
                    print('A stalagmite has fallen on you! It was a glancing blow, but you take some damage.')
                    print()


class kGrove(Room):
    """
    The kelp grove. You don't know how the plants manage to stay alive underground, but you don't think about it too hard.
    There are many chests buried in the mud here.
    """

    def handleEntry(self, player):
        if self.firstEntry == True:
            self.handleFirstEntry()
            self.spawnChest()
            if random.random() > 0.2:
                self.items.append(HealRoot())
        elif random.random() > 0.95:
            self.items.append(HealRoot())

class fCliff(Room):
    """
    The phosphorescent cliffs. Glowing blues, yellows and reds dot your vision all around the cave walls, and extend down past your vision.
    Forms move in pockets obscured by darkness, and you get a sinking feeling in your chest.
    """

    def handleEntry(self, player):
        if self.firstEntry == True:
            self.handleFirstEntry()
            if random.random() > 0.2:
                self.items.append(HealFruit())
        elif random.random() > 0.95:
            self.items.append(HealFruit())
        else:
            self.addMonster(weightedRandom(self.spawnTable))


class oGodsShrine(Room):
    """
    A shrine to some god long since forgotten by most. Judging from its gleaming surface, someone has been maintaining it meticulously.
    """
    def __init__(self,description):
        Room.__init__(self,description)
        self.ticker = 0

    def handleEntry(self,player):
        self.ticker += 1
        if self.ticker >= 2:
            self.desc = "The idol that once stood majestic in the shrine's center has since been defaced.\n No one looks like they're going to clean it up."