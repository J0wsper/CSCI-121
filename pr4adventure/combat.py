import os
from item import Weapon, Potion, Shard

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#This just shows the possible options.
def showHelpCombat():
    clear()
    print('You are in combat and cannot take normal actions')
    print('Instead, you can do any of the following:')
    print('attack -- allows you to select whether you will attack with magic or your weapons')
    print('run -- run away from combat, taking you out of combat with the current monster')
    print('use <item> -- allows you to consume items')
    print()
    input('Press enter to continue... ')

def showHelpLoot():
    clear()
    print('You are looting! There are specific commands you can take:')
    print('take <item> -- lets you take the given item. If you give \'all\', take all the items.')
    print('help -- opens this menu!')
    print('hitting enter lets you end the looting.')
    print()
    input('Press enter to continue... ')


#Work on this
def printSituation(player, monster):
    clear()
    print(monster.name+': '+str(monster.health)+'/'+str(monster.maxHealth))
    print()
    print('You: '+str(player.health)+'/'+str(player.maxHealth))
    print()
    print('You can use the following items: ')
    for i in player.items:
        if issubclass(type(i), Potion):
            print('- '+i.name)
    print()
    print('You can attack with the following weapons:')
    for i in player.items:
        if issubclass(type(i), Weapon):
            print('- '+i.name)
    print()
    print('You have '+str(player.spellSlots)+' spell slots available and you know the following spells:')
    for i in player.knownSpells:
        print('- '+i.name)
    print()
    

#Arranges the list of a monster's loop into a dictionary
def arrangeLoot(monster):
    arrangedLoot = {}
    copiedLoot = monster.loot.copy()
    index = 0
    while index < len(copiedLoot):
        if copiedLoot[index].name not in arrangedLoot:
            arrangedLoot[copiedLoot[index].name] = 1
            del copiedLoot[index]
        else:
            index += 1
        sindex = 0
        while sindex < len(copiedLoot):
            if copiedLoot[sindex] in arrangedLoot:
                arrangedLoot[copiedLoot[sindex].name] += 1
            sindex += 1
    return arrangedLoot

#prints the monster's loot
def printLoot(monster):
    arrangedLoot = arrangeLoot(monster)
    print('The '+monster.name+' dropped the following loot: ')
    print()
    for i in arrangedLoot:
        print('- '+i+': '+str(arrangedLoot[i]))


#The loot loop! Let's the player take their items after defeating a monster
def lootLoop(player,monster):
    lootSuccess = False
    while not lootSuccess:
        lootSuccess = True
        clear()
        printLoot(monster)
        print()
        lootRequest = input('What will you do? ')
        lootRequestWords = lootRequest.split()
        if lootRequestWords == []:

            #If they press enter, give the player the opportunity to exit.
            doneLooting = input('Are you done looting? ')
            if doneLooting == 'yes' or '\n':
                break
            else:
                lootSuccess = False

        #Otherwise, let them take items
        else:
            if lootRequestWords[0] == 'take':

                #If they decide to take all, give them all the items.
                if lootRequestWords[1] == 'all':
                    index = 0
                    while monster.loot != []:
                        i = monster.loot[index]
                        if issubclass(type(i), Shard):
                            player.money[i.typing] += 1
                            monster.loot.remove(i)
                        else:
                            player.items.append(i)
                            monster.loot.remove(i)
                    print('You took all the monster\'s items!')
                    print()
                    input('Press enter to continue... ')
                    lootSuccess = False
                
                #Otherwise, give them a specific item.
                elif monster.getItemByNameLoot(' '.join(lootRequestWords[1:])) in monster.loot:
                    activeLoot = monster.getItemByNameLoot(' '.join(lootRequestWords[1:]))
                    if issubclass(type(activeLoot), Shard):
                        player.money[activeLoot.typing] += 1
                        monster.loot.remove(activeLoot)
                    else:
                        player.items.append(activeLoot)
                        monster.loot.remove(activeLoot)
                    print('You took the monster\'s '+activeLoot.name.lower()+'!')
                    print()
                    input('Press enter to continue... ')
                    lootSuccess = False
                
                #Otherwise, it isn't a valid command.
                else:
                    print('That is not a valid piece of loot.')
                    print()
                    input('Press enter to continue... ')
                    lootSuccess = False
            
            #Gives the player a list of usable commands
            elif lootRequestWords[0] == 'help':
                showHelpLoot()
                lootSuccess = False

            #Otherwise, that isn't a valid command
            else:
                print('That is not a valid command')
                print()
                input('Press enter to continue... ')
                lootSuccess = False


#This is the main combat loop! This handles essentially everything combat-related.
#It has a bunch of helper functions which either live in this doc or in the player/monster docs.

def run(player, monster):
    player.engagedStatus = False
    monster.attackPlayer(player)
    if player.health <= 0:
        player.alive = False
    clear()
    print('You managed to get away, but not without a few scratches...')
    print()
    input('Press enter to continue... ')

def combatLoop(player,monster):
    commandSuccess = False
    while not commandSuccess:
        if player.health <= 0:
            #Work on this
            player.alive = False
            break
        if monster.health <= 0:
            #If the player wins the fight, break and let them take their loot.
            commandSuccess = True
            player.xp += monster.level
            monster.die()
            clear()
            print('You defeated the '+monster.name+'!')
            print()
            input('Press enter to continue... ')
            lootLoop(player,monster)
            if player.xp >= 3*(player.level-1):
                player.levelUp()
        else:
            #Otherwise, run the loop until the combat is over.
            commandSuccess = True
            printSituation(player, monster)
            command = input("How do you respond? ")
            commandWords = command.split()
            
            #Ensuring the game doesn't instantly crash if you just hit enter
            if commandWords == []:
                print("You are engaged in combat, you cannot cancel out!")
                print()
                input('Press enter to continue... ')
                commandSuccess = False
            
            #If you decide to attack the monster:
            elif commandWords[0].lower() == "attack":
                attackSuccess = False

                #This starts its own attack loop, which you can cancel out of by hitting 'enter'.
                #The attack loop allows you to decide if you want to hit the monster with a physical weapon or a spell.
                while not attackSuccess:
                    attackSuccess = True
                    attackCommand = input("Will you attack with your magic or your might? ")
                    attackCommandWords = attackCommand.split()

                    #Allows the player to hit 'enter' if they want to change their gameplan.
                    if attackCommandWords == []:
                        break

                    #If the player wants to cast a spell:
                    elif attackCommandWords[0].lower() == 'magic':
                        spellChoice = input('You\'ve chosen to fight with your magic! Which spell will you use? ')
                        spellChoiceWords = spellChoice.split()
                        
                        #If you hit 'enter', go back a stage.
                        if spellChoiceWords == []:
                            attackSuccess = False

                        #Otherwise, if the spell is a valid spell:
                        elif player.getSpellByName(spellChoice) in player.knownSpells:
                            activeSpell = player.getSpellByName(spellChoice)

                            #Call the magicAttack function in the player class
                            player.magicAttack(monster,activeSpell)

                            #And give the monster its turn to attack
                            monster.attackPlayer(player)

                            input('Press enter to continue... ')

                        #Otherwise, it is not a valid spell.
                        else:
                            print('That is not a valid spell. ')
                            attackSuccess = False

                    #Otherwise, if the player wants to attack with physical weapons:
                    elif attackCommandWords[0].lower() == 'might':
                        weaponChoice = input('You\'ve chosen to fight with your might! Which weapon will you use? ')
                        weaponChoiceWords = weaponChoice.split()
                        
                        #Likewise for breaking out of a loop
                        if weaponChoiceWords == []:
                            attackSuccess = False

                        #If the player has the item they are requesting AND that item is a weapon:
                        elif player.getItemByName(weaponChoice) in player.items and issubclass(type(player.getItemByName(weaponChoice)), Weapon):
                            activeWeapon = player.getItemByName(weaponChoice)
                            
                            #Call on the physAttack function in the player document.
                            player.physAttack(monster,activeWeapon)

                            #Then let the monster attack in turn
                            monster.attackPlayer(player)

                            input('Press enter to continue... ')
                        
                        #Otherwise, you aren't doing it right shithead!
                        else:
                            print('That is not a valid weapon. ')
                            print()
                            input('Press enter to continue... ')
                            attackSuccess = False
                    else:
                        print("Not a valid command")
                        print()
                        input('Press enter to continue... ')
                        commandSuccess = False
                commandSuccess = False
            
            #If you decide to run from the monster:
            elif commandWords[0].lower() == 'run':
                run(player, monster)

            #If you decide to use an item in combat:
            elif commandWords[0].lower() == 'use':
                requestedItem = (' '.join(commandWords[1:])).lower()
                if player.getItemByName(requestedItem) in player.items and issubclass(type(player.getItemByName(' '.join(commandWords[1:]).lower())), Potion) is True:
                    activeItem = player.getItemByName(' '.join(commandWords[1:]).lower())
                    
                    #Lets the player use their active item
                    activeItem.use(player)

                    #At the cost of the monster getting to attack the player.
                    monster.attackPlayer(player)
                    commandSuccess = False
                else:
                    print('That is not a valid item. ')
                    commandSuccess = False
            
            #If you need to pull up the help screen during combat:
            elif commandWords[0].lower() == 'help':
                showHelpCombat()
                commandSuccess = False
            
            #Otherwise, you aren't doing it right!
            else:
                print('Invalid command')
                commandSuccess = False