from room import *
from player import Player
from item import *
from monster import Knight
from combat import combatLoop
from inventory import inventoryLoop, talkLoop
import os
import updater
import random

player = Player()

def createWorld():
    a = oGodsShrine("Room 1. A shrine to some god long since forgotten by most. \n \
    Judging from its gleaming surface, someone has been maintaining it meticulously.")
    b = mDelta("Room 2. You are in the mycelium delta. A room full of mushrooms and fungi, with a miasma of spores obscuring your vision.\n \
        You can feel a shortness in your breath the longer you stay in here.")
    c = mDelta("Room 3. You are in the mycelium delta. A room full of mushrooms and fungi, with a miasma of spores obscuring your vision.\n \
        You can feel a shortness in your breath the longer you stay in here.")
    d = mDelta("Room 4. You are in the mycelium delta. A room full of mushrooms and fungi, with a miasma of spores obscuring your vision.\n \
        You can feel a shortness in your breath the longer you stay in here.")
    e = uRiver("Room 5. The underground river. Villages dot the area, all harvesting their bounty from the river's generosity.\n \
    The river air heals you, but you sense that you will find more monsters in this area.", 'ground')
    f = uRiver("Room 6. The underground river. Villages dot the area, all harvesting their bounty from the river's generosity.\n \
    The river air heals you, but you sense that you will find more monsters in this area.", 'steel')
    g = uRiver("Room 7. The underground river. Villages dot the area, all harvesting their bounty from the river's generosity.\n \
    The river air heals you, but you sense that you will find more monsters in this area.", 'ground')
    h = uRiver("Room 8. The underground river. Villages dot the area, all harvesting their bounty from the river's generosity.\n \
    The river air heals you, but you sense that you will find more monsters in this area.", 'dark')
    i = sWaste("The salt wastes. You don't see any monsters here, probably because they hate the inhospitable soil.\n \
    You think this is a safe place to rest.")
    j = sWaste("The salt wastes. You don't see any monsters here, probably because they hate the inhospitable soil.\n \
    You think this is a safe place to rest.")
    k = sWaste("The salt wastes. You don't see any monsters here, probably because they hate the inhospitable soil.\n \
    You think this is a safe place to rest.")
    l = sWaste("The salt wastes. You don't see any monsters here, probably because they hate the inhospitable soil.\n \
    You think this is a safe place to rest.")
    m = fCliff("The phosphorescent cliffs. Glowing blues, yellows and reds dot your vision all around the cave walls, and extend down past your vision.\n \
    Forms move in pockets obscured by darkness, and you get a sinking feeling in your chest.")
    n = fCliff("The phosphorescent cliffs. Glowing blues, yellows and reds dot your vision all around the cave walls, and extend down past your vision.\n \
    Forms move in pockets obscured by darkness, and you get a sinking feeling in your chest.")
    o = fCliff("The phosphorescent cliffs. Glowing blues, yellows and reds dot your vision all around the cave walls, and extend down past your vision.\n \
    Forms move in pockets obscured by darkness, and you get a sinking feeling in your chest.")
    p = fCliff("The phosphorescent cliffs. Glowing blues, yellows and reds dot your vision all around the cave walls, and extend down past your vision.\n \
    Forms move in pockets obscured by darkness, and you get a sinking feeling in your chest.")
    q = kGrove("The kelp grove. You don't know how the plants manage to stay alive underground, but you don't think about it too hard.\n \
    There are many chests buried in the mud here.")
    r = kGrove("The kelp grove. You don't know how the plants manage to stay alive underground, but you don't think about it too hard.\n \
    There are many chests buried in the mud here.")
    cons = [b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r]
    random.shuffle(cons)
    #Establish the base case, where the first room has a single connection to the entrance of the dungeon.
    a.updateDif(1)
    index = 1
    #Establish the difficulty.
    for i in cons:
        difIndex = ceil(index/4)
        i.updateDif(difIndex)
        index += 1
    Room.connectRooms(a,"north",cons[1],"south")
    dir1 = random.choice(['east','west','north'])
    Room.connectRooms(cons[1], dir1, cons[2], opDir(dir1))
    index = 2
    prevDir = dir1
    while index < len(cons)-1:
        #Create the 'spine' of the room, where each room only has 2 connections: the one before it and the one after it. 
        #Essentially a DLinkedList.
        nextDirOps = ['north','east','west','south']
        nextDirOps.remove(opDir(prevDir))
        nextDir = random.choice(nextDirOps)
        Room.connectRooms(cons[index], nextDir, cons[index+1], opDir(nextDir))
        prevDir = nextDir
        index += 1
    for i in cons:
        cons.remove(i)
        #After the spine has been constructed, add additional connections between the rooms.
        bridgeCon = random.choice(cons)
        if random.random() > 0.4 and bridgeCon != i:
            if bridgeCon not in i.exits and i.dif <=  bridgeCon.dif:
                nextDirOps = ['north','east','west','south']
                for p in i.exitNames():
                    #Checking which direction the new exit will be
                    if p in nextDirOps:
                        nextDirOps.remove(p)
                nextDirOps2 = ['north','east','west','south']
                for p in bridgeCon.exitNames():
                    #Checking which direction the new exit will lead to
                    if p in nextDirOps2:
                        nextDirOps2.remove(p)
                if len(nextDirOps2) > 0 and len(nextDirOps) > 0:  
                    #Ensuring that there are still open options 
                    nextDir = random.choice(nextDirOps)
                    nextDir2 = random.choice(nextDirOps2)
                    Room.connectRooms(i, nextDir, bridgeCon, nextDir2)
        cons.append(i)
        benches = 0
    while benches < len(cons)//4:
        random.choice(cons).addItem(Bench())
        benches += 1


    player.location = a
    startChest = Chest('Starter Chest', 'A chest', [Ironskin(), Leather(), CRobes(), BluePotion()], False)
    a.addItem(startChest)
    a.addItem(Bench())
    if player.typing == 'ground':
        player.learnSpell(Earthquake())
        startChest.contents.append(Claymore())
        player.money['ground'] = 10
        a.addMonster(Scrap(a))
    elif player.typing == 'steel':
        player.learnSpell(FlashCannon())
        startChest.contents.append(Scimitar())
        player.money['steel'] = 10
        a.addMonster(Warlock(a))
    else:
        player.learnSpell(ShadowDance())
        startChest.contents.append(Knife())
        player.money['dark']
        a.addMonster(Mole(a))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Goofy little helper function
def opDir(dir):
    if dir == 'east':
        return 'west'
    elif dir == 'west':
        return 'east'
    elif dir == 'north':
        return 'south'
    else:
        return 'north'

#This is for the overworld when the game tells the player their options.
def printSituation():
    clear()
    print(player.location.desc)
    print()
    if player.location.hasMonsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.hasItems():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can go in the following directions:")
    for e in player.location.exitNames():
        print(e)
    print()

def showHelp():
    clear()
    print("go <direction> -- moves you in the given direction")
    print('attack <monster> -- lets you attack a monster in your current room')
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    print("rest -- allows you to rest at a bench")
    print('me -- shows your current status')
    print('open <chest> -- lets you open a chest in your current room')
    print()
    input("Press enter to continue...")

def me():
    clear()
    print('Your level is '+str(player.level))
    print('Current xp: '+str(player.xp)+'/'+str(3*(player.level)))
    print('Your typing is '+str(player.typing)+'.')
    print('Your health is '+str(player.health)+'/'+str(player.maxHealth)+'.')
    print()
    print('Your stats are: ')
    print('- Attack: '+str(player.Atk))
    print('- Defense: '+str(player.Def))
    print('- Special Attack: '+str(player.SpAtk))
    print('- Special Defense: '+str(player.SpDef))
    print()
    print('Your active armor is: ')
    if len(player.armor) == 1:
        print('- '+player.armor[0].name)
    else:
        for i in player.armor:
            if i.name.lower() != 'exoskeleton':
                print('- '+i.name)
    print()
    input('Press enter to continue...')

createWorld()
worldTimer = 0
playing = True
engaged = False
while playing and player.alive and player.level < 10:
    commandSuccess = False
    timePasses = False  
    printSituation()
    while not commandSuccess:
        commandSuccess = True
        command = input("What now? ")
        commandWords = command.split()

        #Ensuring the game doesn't crash if given an empty command

        if commandWords == []:
            print("Not a valid command")
            commandSuccess = False

        #Allows the player to go places.

        else:
            if commandWords[0].lower() == "go":   #cannot handle multi-word directions
                if commandWords[1] in player.location.exitNames():
                    player.goDirection(commandWords[1]) 
                    timePasses = True
                else:
                    print('Not a valid direction')
                    print()
                    input('Press enter to continue... ')
                    commandSuccess = False

            #Pick up an object.

            elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
                targetName = command[7:]
                target = player.location.getItemByName(targetName)
                if target != False and target.movable == True:
                    player.pickup(target)
                else:
                    print("Invalid item.")
                    commandSuccess = False

            #Shows the inventory.                

            elif commandWords[0].lower() == "inventory":
                inventoryLoop(player)

            #This is the open command.

            elif commandWords[0].lower() == "open":
                if player.location.hasItems() == False:
                    print('There are no items to open here')
                    print()
                    input('Press enter to continue... ')
                    commandSuccess = False
                elif type(player.location.getItemByName(' '.join(commandWords[1:]))) is Chest:
                    activeChest = player.location.getItemByName(' '.join(commandWords[1:]))
                    activeChest.chestLoop(player)
                else:
                    print('That item cannot be opened. ')
                    print()
                    input('Press enter to continue... ')

            #Simple help command.

            elif commandWords[0].lower() == "help":
                showHelp()

            #Simple exit command to end the game.

            elif commandWords[0].lower() == "exit":
                playing = False

            #This is the attack loop. It's mostly just passed off to combat.py

            elif commandWords[0].lower() == "attack":
                targetName = command[7:]
                target = player.location.getMonsterByName(targetName)
                if targetName == '':
                    print("No such monster.")
                    print()
                    input('Press enter to continue... ')
                    commandSuccess = False
                elif target != False and target.health > 0:
                    clear()
                    print('You attacked the '+targetName+'!')
                    combatLoop(player,target)
                else:
                    print("No such monster.")
                    print()
                    input('Press enter to continue... ')
                    commandSuccess = False

            #Returns the player's current status.

            elif commandWords[0].lower() == "me":
                me()

            elif commandWords[0].lower() == 'talk':
                activeMonster = player.location.getMonsterByName(' '.join(commandWords[1:]))
                if activeMonster in player.location.monsters:
                    if activeMonster.aggroType(player.typing) != 0:
                        player.engagedStatus = True
                        clear()
                        print('The '+activeMonster.name+' did not want to talk!')
                        print('You were attacked by the '+activeMonster.name+'!')
                        combatLoop(player, activeMonster)
                    else:
                        talkLoop(player, activeMonster)
                else:
                    print('No such monster.')
                    print()
                    input('Press enter to continue... ')
                    commandSuccess = False

            #Allows the user to meditate to regain health.

            elif commandWords[0].lower() == 'rest' and player.location.getItemByName('Bench') != False:
                player.location.getItemByName('Bench').rest(player)
            else:
                print("Not a valid command")
                print()
                input('Press enter to continue... ')
                commandSuccess = False

    #This is where all of the game updates happen. If you want something to happen as time passes,
    #put it in here.
    if timePasses == True:
        updater.updateAll()

        #Handles specific room effects
        player.location.handleEntry(player)

        #This loop handles monster interaction
        if player.location.hasMonsters() is True:
            for i in player.location.monsters:
                i.handleAttack(player)
            if player.engagedStatus == True:
                for i in player.location.monsters:
                    if i.engagedStatus == True:
                        print('You were attacked by a hostile '+i.name+'!')
                        print()
                        input('Press enter to continue... ')
                        combatLoop(player,i)
        
        #Handle potion effects
        for i in player.activePotions:
            i.update(player)

if player.alive == False:
    print(player.health)
    print('You died... ')
    print()
    input('Press enter to continue... ')
if player.level >= 10:
    print('You won!')
    print()
    input('Thank you for playing. ')