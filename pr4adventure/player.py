import os
import random
from item import Armor, damageCalc, Shard, Earthquake, StoneEdge, Magnitude, ShadowDance, DarkPulse, Torrent, FlashCannon, Rain, StarScream
from math import floor

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def hpCalc(base, level):
    return floor((((base+31)*2)*level)/(100)+level+10)

def statCalc(base,level):
    return floor((((base+31)*2)*level)/(100)+5)

class Player:

    #The player's __init__ is a bit of a fucking nightmare! But! Fortunately, most of this stuff is pretty sensible.
    def __init__(self):
        self.location = None
        self.engagedStatus = False
        self.items = []
        self.activePotions = []
        self.maxSlots = 1
        self.spellSlots = self.maxSlots
        self.level = 1
        self.xp = 0
        self.money = {'ground':0,'steel':0,'dark':0}
        self.Atk = statCalc(100, self.level+1)
        self.SpAtk = statCalc(100, self.level+1)
        self.Def = statCalc(100, self.level+1)
        self.SpDef = statCalc(100, self.level+1)
        self.maxHealth = hpCalc(100, self.level+1)
        self.health = self.maxHealth
        self.alive = True
        self.typing = random.choice(['dark','steel','ground'])
        self.knownSpells = []
        self.armor = [Armor('Exoskeleton','Your own exoskeleton', 2, 2, 2, 2, 10)]

    #Allows the player to walk around
    def goDirection(self, direction):
        self.location = self.location.getDestination(direction)
    
    def spellHelper(self):
        assert(self.level%3 == 0)
        if self.level//3 == 1:
            if self.typing == 'steel':
                return Earthquake()
            elif self.typing == 'dark':
                return FlashCannon()
            else:
                return ShadowDance()
        elif self.level//3 == 2:
            if self.typing == 'steel':
                return StoneEdge()
            elif self.typing == 'dark':
                return Rain()
            else:
                return DarkPulse()
        elif self.level//3 == 3:
            if self.typing == 'steel':
                return Magnitude()
            elif self.typing == 'dark':
                return StarScream()
            else:
                return Torrent()

    #Function that lets you add spells to the player's known spells
    def learnSpell(self,spell):
        self.knownSpells.append(spell)

    #Lets you pickup items in the terrain
    def pickup(self, item):
        if issubclass(type(item), Shard):
            self.money[item.typing] += 1
            self.location.removeItem(item)
        else:
            self.items.append(item)
            item.loc = self
            self.location.removeItem(item)

    #Lets you drop items onto the terrain!
    def drop(self,item):
        self.items.remove(item)
        item.loc = self.location

    def activeArmor(self):
        if len(self.armor) == 1:
            activeArmor = self.armor[0]
        else:
            activeArmor = self.armor[0]
            for i in self.armor:
                if i.name.lower() != 'exoskeleton':
                    activeArmor = i
        return activeArmor

    #Physical attack! This is what is called when the player decides to fight with 'might'.
    def physAttack(self,monster,weapon):

        #Checking to see if the player's attack misses based on the monster's evasion.
        if random.random() < monster.evasion//100:
            print('Your attack missed!')

        #If the attack did hit:
        else:

            #Checking to see if the attack was a crit (change this)
            if random.random() > 0.99:
                print('Critical hit!')
                monster.health -= 2*damageCalc(weapon, self, monster, 'physical')
            
            #Otherwise, a normal hit is landed
            else:
                print('You hit the '+monster.name+'!')
                weapon.attack(self, monster)


    #This is the magic attack! This is what is called when the player fights with magic
    def magicAttack(self,monster,spell):

        #If you have no spell slots, you can't cast
        if self.spellSlots <= 0:
            print('You are all out of spell slots! ')
            input('Press enter to continue... ')

        #Otherwise:
        else:

            #Checking to see if you beat the target's evasion.
            if random.random() < monster.evasion//100:
                print('The '+spell.name+' missed! ')

            #If you do:
            else:

                #The spell goes off normally, and the spell.cast() function is called.
                print('Your '+spell.name+' hit the '+monster.name+'!')
                spell.cast(self,monster)


    #Helper function that lets you get an item from its name alone.
    def getItemByName(self,name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i

    def getArmorByName(self,name):
        for i in self.armor:
            if i.name.lower() == name.lower():
                return i

    #More helpers
    def printInventory(self):
        inventoryList = []
        for i in self.items:
            inventoryList.append(i.name.lower())
        return inventoryList

    def printArmor(self):
        armorList = []
        for i in self.armor:
            armorList.append(i.name.lower())
        return armorList

    #Yet more helpers
    def getSpellByName(self,spell):
        for i in self.knownSpells:
            if i.name.lower() == spell.lower():
                return i

    def levelUp(self):
        self.xp = 0
        self.level += 1
        self.Atk = statCalc(100, self.level+1)+self.activeArmor().Atk
        self.SpAtk = statCalc(100, self.level+1)+self.activeArmor().SpAtk
        self.Def = statCalc(100, self.level+1)+self.activeArmor().Def
        self.SpDef = statCalc(100, self.level+1)+self.activeArmor().SpDef
        self.maxHealth = hpCalc(100, self.level+1)
        if self.level%3 == 0:
            self.spellSlots += 1
            self.learnSpell(self.spellHelper())
        clear()
        print('You leveled up to level '+str(self.level-1)+'!')
        print('Your stats have increased to reflect your growth.')
        input('Press enter to continue... ')

        