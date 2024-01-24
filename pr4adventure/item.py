import os
import updater
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def supEffect(attack,target):
        if (target.typing == 'dark' and attack.typing == 'steel') or (target.typing == 'steel' and attack.typing == 'ground')\
         or (target.typing == 'ground' and attack.typing == 'dark'):
            return True
        else:
            return False

def handleSecEffect(attack,user,target):
    if attack.secEffect == True:
        attack.resolveSecEffect(user,target)

def damageHelper(level, power, attack, defense):
    return int(((((10*level)/5*power*(attack/defense))/50)+2))

def weightedRandom(dct):
    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        total += v
        if rand_val <= total:
            return k
    assert False, 'unreachable'


#This calculates damage! It is used on an item (either a weapon or a spell), and is passed the user, the target and whether the attack is 'special' (a spell),
#or if it is 'physical' (a weapon). It then calculates damage in the standard Pokemon way, incorporating STAB as well
def damageCalc(attackingItem,user,target,stat):
        assert(stat == 'special' or stat == 'physical')
        assert(issubclass(type(attackingItem), Weapon) or issubclass(type(attackingItem), Spell))
        if attackingItem.typing == user.typing:
            STAB = 1.5
        else:
            STAB = 1
        if supEffect(attackingItem, target) == True:
            typeBonus = 1.5
        else:
            typeBonus = 0.75
        if stat.lower() == 'special':
            damage = int(STAB*typeBonus*damageHelper(user.level, attackingItem.power, user.SpAtk, target.SpDef))
        else:
            damage = int(STAB*typeBonus*damageHelper(user.level, attackingItem.power, user.Atk, target.Def))
        return damage

def damageCalcText(attackingItem, target):
    if supEffect(attackingItem, target) == True:
        return 'It was super effective!'
    else:
        return 'It was not very effective...'

class Item:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.price = 0
        self.loc = None
        self.movable = True
    
    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    
    def putInRoom(self, room):
        self.loc = room
        room.addItem(self)

#Chest class! Holds things
class Chest(Item):

    def __init__(self, name, desc, contents, lockedStatus):
        Item.__init__(self,name,desc)
        self.contents = contents
        self.lockedStatus = lockedStatus
        self.openStatus = False
        self.movable = False

    def getItemByName(self, name):
        for i in self.contents:
            if i.name.lower() == name.lower():
                return i

    #Open is the command that lets the player actually see the contents of the chest.
    def open(self):
        if self.lockedStatus == True:
            print('The chest is locked.')
        else:
            print('The chest has been opened')
            self.openStatus = True

    #Deposit is a command that lets the player move an item from their inventory to the chest.
    def deposit(self, player, object):
        if self.openStatus == False and self.lockedStatus == True:
            return 'The chest is locked, you can\'t put objects in here'
        elif self.openStatus == False and self.lockedStatus == False:
            return 'You have to open the chest first'
        elif self.openStatus == True and object in player.items:
            self.contents.append(object)
            player.items.remove(object)
            clear()
            print('The '+object.name+' has been placed in the chest.')
            print()
            input('Press enter to continue... ')
        else:
            clear()
            print('That item is not in your inventory. ')
            print()
            input('Press enter to continue... ')
    
    #Take is the opposite of deposit. It lets the player take items from the chest into their inventory.
    def take(self, player, object):
        if self.openStatus == False and self.lockedStatus == True:
            return 'The chest is locked, you can\'t put objects in here'
        elif self.openStatus == False and self.lockedStatus == False:
            return 'You have to open the chest first'
        elif self.openStatus == True:
            if object == 'all':
                index = 0
                while self.contents != []:
                    i = self.contents[index]
                    if issubclass(type(i), Shard):
                        player.money[i.typing] += 1
                        self.contents.remove(i)
                    else:
                        player.items.append(i)
                        self.contents.remove(i)
                clear()
                print('You have taken everything from the chest.')
                print()
                input('Press enter to continue... ')
            elif object in self.contents:
                if issubclass(type(object), Shard):
                        player.money[object.typing] += 1
                        self.contents.remove(object)
                else:
                    player.items.append(object)
                    self.contents.remove(object)
                clear()
                print('The '+object.name+' has been withdrawn from the chest.')
                print()
                input('Press enter to continue... ')
        else:
            print('That object is not in this chest')
            print()
            input('Press enter to continue...')

    def printContents(self):
        contentsName = []
        for i in self.contents:
            contentsName.append(i.name.lower())
        return contentsName
    
    def chestLoop(self, player):
        if type(self) is Chest:
            chestOpening = False
            self.open()

            #This is the chest loop!

            while not chestOpening:
                chestOpening = True
                print('The contents of the chest are:')
                for i in self.contents:
                    print('- '+i.name)
                takeDropRequest = input('Would you like to take or deposit anything? ')
                takeDropRequestWords = takeDropRequest.split()
                requestedItem = ' '.join(takeDropRequestWords[1:])
                if takeDropRequest == '':
                    break
                elif takeDropRequestWords[0] == 'take':
                    if requestedItem == 'all':
                        self.take(player,'all')
                    elif requestedItem in self.printContents():
                        #If they want to deposit an item, take them to the helper function.
                        self.take(player,self.getItemByName(requestedItem))
                        chestOpening = False
                    else:
                        print('That is not a valid item')
                        print()
                        input('Press enter to continue... ')
                elif takeDropRequestWords[0] == 'deposit' and requestedItem in player.printInventory():

                    #Otherwise, if they want to take an item, it directs them to the take function.
                    self.deposit(player,player.getItemByName(requestedItem))
                    chestOpening = False
                else:
                    print('Invalid command')
                    chestOpening = False

        else:
            print('That is not a chest')
            chestOpening = False

class Bench(Item):

    def __init__(self):
        Item.__init__(self, 'Bench', 'A creaky wooden bench')
        self.movable = False
    
    def rest(self, player):
        player.health = player.maxHealth
        player.spellSlots = player.maxSlots
        index = 0
        while index < 5:
            updater.updateAll()
            index += 1
        print('You rest for a moment and dress your wounds.')
        print()
        input('Press enter to continue... ')

#Weapons! These are what the player will use to enable their physical attack
class Weapon(Item):

    def __init__(self, name, desc, power, typing, secEffect, evasion):
        Item.__init__(self,name,desc)
        self.power = power
        if typing is None:
            self.typing = random.choice(['ground','steel','dark'])
        else:
            self.typing = typing
        self.secEffect = secEffect
        self.evasion = evasion
    
    def resolveSecEffect(self, user, target):
        pass
    
    def attack(self, user, target):
        target.health -= damageCalc(self, user, target, 'physical')
        print(damageCalcText(self, target))
        handleSecEffect(self, user, target)

#Spells! These are what the player will use to enable their special attack
class Spell(Item):
    
    def __init__(self, name, desc, power, typing, secEffect):
        Item.__init__(self,name,desc)
        self.power = power
        self.typing = typing
        self.secEffect = secEffect

    #This is the cast function! It is the main thing for Spells.
    def cast(self,player,target):
        assert(player.spellSlots > 0)
        player.spellSlots -= 1
        target.health -= damageCalc(self, player, target, 'special')
        print(damageCalcText(self, target))
        handleSecEffect(self, player, target)

#Armor! This can increase the player's physical defense.
class Armor(Item):

    #Each armor contributes its own Atk, SpAtk, Def and SpDef bonuses to the player, as well as an evasion.
    def __init__(self,name,desc,Atk,SpAtk,Def,SpDef,evasion):
        Item.__init__(self,name,desc)
        self.Atk = Atk
        self.SpAtk = SpAtk
        self.Def = Def
        self.SpDef = SpDef
        self.evasion = evasion

    #Don lets the player put on different armors.
    def don(self,player):
        if self in player.items and len(player.armor) < 2:
            player.items.remove(self)
            player.armor.append(self)
            player.Atk += self.Atk
            player.SpAtk += self.SpAtk
            player.Def += self.Def
            player.SpDef += self.SpDef
            print('You donned the '+self.name+'!')
            print()
            input('Press enter to continue... ')
        #Ensures the player can't wear more than one piece of armor at once.
        #The reason that there are 2 armors is because the Exoskeleton, the basic armor, cannot be discarded.
        elif len(player.armor) >= 2:
            print('You cannot have more than one piece of armor on at a time.')
            print()
            input('Press enter to continue... ')
        else:
            print('That cannot be donned. ')
            print()
            input('Press enter to continue... ')

    #Doff lets the player take off various armors.
    def doff(self,player):
        if self in player.armor and self.name.lower() != 'exoskeleton':
            player.armor.remove(self)
            player.items.append(self)
            player.Atk -= self.Atk
            player.SpAtk -= self.SpAtk
            player.Def -= self.Def
            player.SpDef -= self.SpDef
            clear()
            print('You doffed the '+self.name+'!')
            print()
            input('Press enter to continue... ')
        #If the armor they are trying to doff is the exoskeleton, don't!
        elif self.name.lower() == 'exoskeleton':
            clear()
            print('You cannot doff your own exoskeleton.')
            print()
            input('Press enter to continue... ')
        else:
            clear()
            print('That cannot be doffed. ')
            print()
            input('Press enter to continue... ')

#Potion class! Essentially just consumables.
class Potion(Item):

    #secEffect shold be true or false. If it is false, then you don't need to define a secondary effect.
    #If it is true, then a secondary effect function needs to be defined
    def __init__(self, name, desc, healing, secEffect):
        Item.__init__(self,name,desc)
        self.healing = healing
        self.secEffect = secEffect
    
    #Used to ensure we don't get any game-breaking bugs
    def handleSecEffect(self,player):
        if self.secEffect == True:
            player.activePotions.append(self)

    #This is the main function! It is called when a player wants to use a potion.
    def use(self,player):
        print('You drank the potion and gained its effect! ')
        if self.healing > player.maxHealth - player.health:
            self.healing = player.maxHealth - player.health
        player.health += self.healing
        player.items.remove(self)
        self.handleSecEffect(player)

class Shard(Item):

    def __init__(self, name, desc):
        Item.__init__(self,name, desc)
        self.price = 1

#Everything below this point involves specific subclasses of the above classes.
class Leather(Armor):

    def __init__(self):
        Armor.__init__(self, 'Leather armor', 'Armor made from tanned leather', 5, 3, 5, 3, 10)
        self.price = 3

class CRobes(Armor):

    def __init__(self):
        Armor.__init__(self, 'Cultist Robes', 'Shabby robes stained with... something', 3, 5, 3, 5, 10)
        self.price = 3

class Plate(Armor):

    def __init__(self):
        Armor.__init__(self, 'Plate armor', 'Steel armor made from interlocking plates', 10, 5, 10, 5, 20)
        self.price = 10

class WRobes(Armor):

    def __init__(self):
        Armor.__init__(self, 'Wizard Robes', 'Embroidered blue robes with swirling patterns', 5, 10, 5, 10, 20)
        self.price = 10

class Calci(Armor):

    def __init__(self):
        Armor.__init__(self, 'Calcifex', 'An armor made of living bone. Very pointy', 20, 10, 20, 10, 30)
        self.price = 30

class Hemo(Armor):

    def __init__(self):
        Armor.__init__(self, 'Hemophage', 'Robes of deep red, whispering foul incantations', 10, 20, 10, 20, 30)
        self.price = 30

class ShadowCloak(Armor):

    def __init__(self):
        Armor.__init__(self, 'Shadow cloak', 'Armor that bends light around it',  10, 10, 0, 0, 100)
        self.price = 1000

#Below are all the specific weapons
class Scimitar(Weapon):

    def __init__(self):
        Weapon.__init__(self,'Scimitar','A curved blade. More likely to land a critical hit.', 20, 'steel', True, 10)
        self.price = 3
    
class Cudgel(Weapon):
    
    def __init__(self, typing):
        Weapon.__init__(self, 'Cudgel', 'A simple curved stick imbued with magic.', 10, typing, False, 5)
        self.price = 1
    
class Knife(Weapon):

    def __init__(self):
        Weapon.__init__(self, 'Knife', 'A wicked knife of dark metal.', 20, 'dark', False, 10)
        self.price = 3

class Claymore(Weapon):

    def __init__(self):
        Weapon.__init__(self, 'Claymore', 'A large steel sword', 20, 'ground', False, 10)
        self.price = 3

class GreatSword(Weapon):

    def __init__(self):
        Weapon.__init__(self, 'Greatsword', 'An enormous, chipped blade', 40, 'steel', False, 10)
        self.price = 10

class Flail(Weapon):

    def __init__(self):
        Weapon.__init__(self, 'Flail', 'A dirty, brutal flail', 40, 'ground', False, 10)
        self.price = 10

class Cleaver(Weapon):

    def __init__(self):
        Weapon.__init__(self, 'Cleaver', 'A brutal square blade', 40, 'dark', False, 10)
        self.price = 10

class Plague(Weapon):

    def __init__(self):
        Weapon.__init__(self, 'Plague', 'A legendary sword, coated in poison', 60, 'ground', False, 10)
        self.price = 30

class Woe(Weapon):

    def __init__(self):
        Weapon.__init__(self, 'Woe', 'A blade that eats all light', 60, 'dark', False, 10)
        self.price = 30

class Flayer(Weapon):

    def __init__(self):
        Weapon.__init__(self, 'Flayer', 'A pearless blade of shining steel', 60, 'steel', False, 10)
        self.price = 30

#Below are all the specific spells
class Earthquake(Spell):

    def __init__(self):
        Spell.__init__(self,'Earthquake','At your whim, the ground shakes violently',40,'ground', False)

class StoneEdge(Spell):

    def __init__(self):
        Spell.__init__(self, 'Stone Edge', 'A blade of hardened earth erupts from the ground', 60, 'ground', False)

class Magnitude(Spell):

    def __init__(self):
        Spell.__init__(self, 'Magnitude', 'The entire cave vibrates around you with force', 80, 'ground', False)

class ShadowDance(Spell):

    def __init__(self):
        Spell.__init__(self,'Shadow Dance','Calling on the forces of the dark, your shadows attack your enemies',40,'dark',False)
    
class DarkPulse(Spell):

    def __init__(self):
        Spell.__init__(self, 'Dark Pulse', 'A wave of darkness erupts from your hands', 60, 'dark', False)

class Torrent(Spell):

    def __init__(self):
        Spell.__init__(self, 'Torrent', 'The forces of eldritch power spill forth at your will', 80, 'dark', False)

class FlashCannon(Spell):

    def __init__(self):
        Spell.__init__(self,'Flash Cannon','Using your metalurgy, you produce a blinding flash of light',40,'steel',False)

class Rain(Spell):

    def __init__(self):
        Spell.__init__(self, 'Steel Rain', 'Calling on the machine spirit, you make metal rain from the ceiling', 60, 'steel', False)

class StarScream(Spell):

    def __init__(self):
        Spell.__init__(self, 'Star Scream', 'The stars rain down fire, burning your enemies', 80, 'steel', False)


#Shards! These are essentially the currency of the game. There are 3 typings, and their value is based on which type
#the vendor is weak to. For example, if the vendor is a steel type, ground shards will be worth the most.
class gShard(Shard):

    def __init__(self):
        Shard.__init__(self,'Ground Shard','A relic of some long-forgotten ground tribe technology')
        self.typing = 'ground'

class sShard(Shard):

    def __init__(self):
        Shard.__init__(self, 'Steel Shard', 'A relic of some long-forgotten steel metalurgy technology')
        self.typing = 'steel'

class dShard(Shard):

    def __init__(self):
        Shard.__init__(self, 'Dark Shard', 'A relic of some long-forgotten dark arts technology')
        self.typing = 'dark'

#The ironskin potion increases the player's defense for a few rooms
class Ironskin(Potion):

    def __init__(self):
        Potion.__init__(self,'Ironskin Potion','A potion that is supposed to make your skin as tough as metal', 0, True)
        self.timer = 0
        self.price = 7
    
    #Increases the player's defense
    def update(self,player):
        if self.timer == 0:
            player.Def = int(player.Def*1.5)
            self.timer += 1
        elif self.timer > 3:
            player.Def = int(player.Def//1.5)
            player.activePotions.remove(self)
            print('The effects of your ironskin potion have worn off... ')
            print()
            input('Press enter to continue... ')
        else:
            self.timer += 1

class Calm(Potion):
    
    def __init__(self):
        Potion.__init__(self,'Calm Potion','A potion that turns your mind into a fortress', 0, True)
        self.timer = 0
        self.price = 7
    
    #Increases the player's defense
    def update(self,player):
        if self.timer == 0:
            player.SpDef = int(player.SpDef*1.5)
            self.timer += 1
        elif self.timer > 3:
            player.SpDef = int(player.SpDef//1.5)
            player.activePotions.remove(self)
            print('The effects of your ironskin potion have worn off... ')
            print()
            input('Press enter to continue... ')
        else:
            self.timer += 1

class Ration(Potion):

    def __init__(self):
        Potion.__init__(self, 'Ration', 'A simple, soldier\'s meal', 10, False)
        self.price = 3

class HealFruit(Potion):

    def __init__(self):
        Potion.__init__(self, 'Healing Fruit', 'A glowing fruit from the phospohrescent cliffs', 20, False)
        self.price = 3

class HealRoot(Potion):

    def __init__(self):
        Potion.__init__(self, 'Healing Root', 'A gnarled root from the kelp grove', 20, False)
        self.price = 3

class BluePotion(Potion):

    def __init__(self):
        Potion.__init__(self, 'Blue Potion', 'An odd potion with a blueish hue', 0, True)
        self.price = 5

    def update(self, player):
        if player.spellSlots < player.maxSlots:
            player.spellSlots += 1
            player.activePotions.remove(self)
