import random
import updater
from math import *
import os
from item import *

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def hpCalc(base, level):
    return floor((((base+31)*2)*level)/(100)+level+10)

def statCalc(base,level):
    return floor((((base+31)*2)*level)/(100)+5)

class Monster:

    def __init__(self, name, health, Atk, SpAtk, Def, SpDef, evasion, spellSlots, room, typing):
        self.name = name
        self.level = room.dif
        self.Atk = statCalc(Atk, self.level)
        self.SpAtk = statCalc(SpAtk, self.level)
        self.Def = statCalc(Def, self.level)
        self.SpDef = statCalc(SpDef, self.level)
        self.maxHealth = hpCalc(health, self.level)
        self.health = self.maxHealth
        self.evasion = evasion
        self.room = room
        self.loot = []
        self.soldItems = []
        self.weapons = []
        self.spellSlots = spellSlots
        self.knownSpells = []
        self.lines = []
        self.engagedStatus = False
        if typing is None:
            self.typing = random.choice(['dark','steel','ground'])
        else:
            self.typing = typing
        updater.register(self)

    def update(self):
        pass

    def aggroType(self, playerType):
        if (playerType == 'ground' and self.typing == 'steel') or (playerType == 'dark' and self.typing == 'ground')\
            or (playerType == 'steel' and self.typing == 'dark'):
            return 1
        elif (playerType == 'steel' and self.typing == 'ground') or (playerType == 'ground' and self.typing == 'dark')\
            or (playerType == 'dark' and self.typing == 'steel'):
            return 2
        else:
            return 0

    #Helper function to check if a monster will attack the player.
    def handleAttack(self,player):
        if player.location == self.room and self.aggroType(player.typing) == 1:
            player.engagedStatus = True
            self.engagedStatus = True

    #Basic function that kills a monster and removes it from the code.
    def die(self):
        self.room.removeMonster(self)
        if self in updater.updates:
            updater.deregister(self)

    def learnSpell(self,spell):
        self.knownSpells.append(spell)

    def addWeapon(self,weapon):
        self.weapons.append(weapon)

    def attackPlayer(self,player):
        if random.random() < player.activeArmor().evasion/100:
            print('The '+self.name+' missed!')
        else:
            bestWeapon = self.weapons[0]
            for i in self.weapons:
                if damageCalc(i, self, player, 'physical') >= damageCalc(bestWeapon, self, player,'physical'):
                    bestWeapon = i
            if self.knownSpells != []:
                bestSpell = self.knownSpells[0]
                for j in self.knownSpells:
                    if damageCalc(j, self, player, 'special') >= damageCalc(bestSpell, self, player, 'special'):
                        bestSpell = j
                if damageCalc(bestSpell, self, player, 'special') > damageCalc(bestWeapon, self, player, 'physical'):
                    bestOption = bestSpell
                else:
                    bestOption = bestWeapon
            else:
                bestOption = bestWeapon
            if issubclass(type(bestOption), Spell) and self.spellSlots > 0:
                player.health -= damageCalc(bestOption, self, player, 'special')
                self.spellSlots -= 1
                print(player.health)
            else:
                player.health -= damageCalc(bestWeapon, self, player, 'physical')
                print(player.health)
            print('The '+self.name.lower()+' managed to hit you with its '+bestOption.name+'.')

    #Gets an item from its name alone
    def getItemByNameLoot(self, item):
        for i in self.loot:
            if i.name.lower() == item.lower():
                return i
    
    def getItemByNameSold(self, item):
        for i in self.soldItems:
            if i.name.lower() == item.lower():
                return i

#Ground monsters below

#The mole is the most basic class of ground monster
class Mole(Monster):
    
    def __init__(self,room):
        Monster.__init__(self, 'Giant Mole', 40, 20, 0, 10, 20, 10, 0, room, 'ground')
        self.addWeapon(Claymore())
        self.loot.append(gShard())

class Traitor(Monster):

    def __init__(self, room):
        Monster.__init__(self, 'Traitor', 60, 30, 30, 30, 30, 10, 1, room, 'ground')
        self.knownSpells.append(Earthquake())
        self.addWeapon(Flail())

class Orogene(Monster):

    def __init__(self, room):
        Monster.__init__(self, 'Orogene', 80, 60, 60, 50, 50, 20, 3, room, 'ground')
        self.knownSpells.append(StoneEdge())
        self.addWeapon(Plague())

#Steel monsters below

#The knight is the most basic class of steel monster
class Scrap(Monster):

    def __init__(self,room):
        Monster.__init__(self, 'Living Scrap', 40, 50, 30, 10, 20, 5, 0, room, 'steel')
        self.addWeapon(Claymore())

class Knight(Monster):

    def __init__(self, room):
        Monster.__init__(self, 'Knight', 60, 60, 10, 50, 30, 10, 0, room, 'steel')
        self.addWeapon(GreatSword())

class Warlord(Monster):

    def __init__(self, room):
        Monster.__init__(self, 'Warlord', 80, 80, 10, 90, 50, 20, 0, room, 'steel')
        self.addWeapon(Flayer())

#Dark monsters below

#The warlock is the most basic class of dark monster
class Warlock(Monster):

    def __init__(self, room):
        Monster.__init__(self, 'Warlock', 40, 20, 30, 20, 40, 10, 1, room, 'dark')
        self.addWeapon(Knife())
        self.learnSpell(ShadowDance())

class Shadow(Monster):

    def __init__(self, room):
        Monster.__init__(self, 'Shade', 60, 20, 50, 60, 20, 10, 3, room, 'dark')
        self.addWeapon(Cleaver())
        self.learnSpell(DarkPulse())

class Omen(Monster):

    def __init__(self, room):
        Monster.__init__(self, 'Omen', 80, 30, 80, 40, 80, 10, 5, room, 'dark')
        self.addWeapon(Woe())
        self.learnSpell(Torrent())

#Special monsters below

class Riverfolk(Monster):

    def __init__(self,room,typing):
        Monster.__init__(self, 'Riverfolk', 40, 25, 5, 20, 10, 5, 1, room, typing)
        self.addWeapon(Cudgel)
