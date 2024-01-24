import updater
import os
import random
from item import Armor, Shard, Potion

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Arrange items allows you to view the items of your inventory in stacks rather than individually!
#It returns a dictionary that is then parsed by the proceeding function
def arrangeItems(player):
    arrangedInventory = {}
    copiedInventory = player.items.copy()
    index = 0
    while index < len(copiedInventory):
        if copiedInventory[index].name not in arrangedInventory:
            arrangedInventory[copiedInventory[index].name] = 1
        else:
            arrangedInventory[copiedInventory[index].name] += 1
        index += 1
    return arrangedInventory

def donOrDoff(player, armorName, donOrDoff):
    if donOrDoff == 'don':
        activeArmor = player.getItemByName(armorName)
        if armorName.lower() in player.printInventory() and issubclass(type(activeArmor), Armor):
            #print(player.printArmor())
            #print(activeArmor.name.lower())
            activeArmor.don(player)
        else:
            print('That is not a valid armor.')
            print()
            input('Press enter to continue... ')
    else:
        activeArmor = player.getArmorByName(armorName)
        if armorName.lower() in player.printArmor() and issubclass(type(activeArmor), Armor):
            activeArmor.doff(player)
        else:
            print('That is not a valid armor.')
            print()
            input('Press enter to continue... ')


#printInventory parses the dictionary handed to it by arrangeItems
def printInventory(player):
    arrangedInventory = arrangeItems(player)
    print('The contents of your inventory are: ')
    for i in arrangedInventory:
        print('- '+i+': '+str(arrangedInventory[i]))
    print()
    print('You have the following shards: ')
    for i in player.money:
        print('- '+i+': '+str(player.money[i]))
    print()


#Welcome to the inventory loop fuckers. This shit loops. It uses the parsed dictionary from printInventory to display the inventory contents.
#Hopefully there will be commands in here eventually that allow the player to do shit.
def inventoryLoop(player):
    commandSuccess = False
    while not commandSuccess:
        clear()
        printInventory(player)
        commandSuccess = True
        inventoryCommand = input('What will you do? ')
        inventoryCommandWords = inventoryCommand.split()
        if inventoryCommandWords == []:
            break
        
        elif inventoryCommandWords[0] == 'doff' or inventoryCommandWords[0] == 'don':
            donOrDoff(player, ' '.join(inventoryCommandWords[1:]), inventoryCommandWords[0])
            commandSuccess = False

        elif inventoryCommandWords[0] == 'use' and issubclass(type(player.getItemByName(' '.join(inventoryCommandWords[1:]))), Potion):
            activeItem = player.getItemByName(' '.join(inventoryCommandWords[1:]))
            activeItem.use(player)
            print()
            input('Press enter to continue... ')
        #Add a crafting option in here eventually


        else:
            print('That is not a valid command.')
            print()
            input('Press enter to continue... ')
            commandSuccess = False

def talkHelp(monster):
        print('talk -- lets you talk to the '+monster.name+'.')
        print('sell <item> -- lets you sell the chosen item.')
        print('buy <item> -- lets you buy the chosen item.')
        print('hit enter to stop talking.')
        print()
        input('Press enter to continue... ')

def countMoney(player, monster):
    money = 0
    for i in player.money:
        if i == monster.typing:
            money += 2*player.money[i]
        else:
            money += player.money[i]
    return money

def printWares(monster):
    print('The '+monster.name.lower()+' is selling the following: ')
    for i in monster.soldItems:
        print('- '+i.name+': '+str(i.price)+' shards')

def playerPay(player, monster, item):
    paid = 0
    for i in player.money:
        if i == monster.typing:
            pref = i
        elif monster.aggroType(i) == 2:
            secPref = i
        else:
            leastPref = i
    while paid <= item.price:
        if player.money[pref] != 0:
            paid += 2
            player.money[pref] -= 1
        elif player.money[secPref] != 0:
            paid += 1
            player.money[secPref] -= 1
        else:
            paid += 1
            player.money[leastPref] -= 1

def monsterPay(player, monster, item):
    paid = 0
    while paid <= item.price:
        player.money[monster.typing] += 1
        paid += 1

#Talking loop!
def talkLoop(player, monster):
        buySuccess = False
        while not buySuccess:
            clear()
            if monster.lines == []:
                print(monster.name+': Lovely weather we\'re having, isn\'t it?')
            else:
                print(monster.name+': '+random.choice(monster.lines))
            print()
            printWares(monster)
            print()
            printInventory(player)
            print(arrangeItems(player))
            buySuccess = True
            buyRequest = input('What would you like to do? ')
            buyRequestWords = buyRequest.split()
            if buyRequestWords == []:
                break
            elif buyRequestWords[0] == 'buy':
                activeItemName = ' '.join(buyRequestWords[1:])
                activeItem = monster.getItemByNameSold(activeItemName)
                if activeItem in monster.soldItems:
                    price = activeItem.price
                    if price <= countMoney(player,monster):
                        playerPay(player, monster, activeItem)
                        monster.soldItems.remove(activeItem)
                        if issubclass(type(activeItem), Shard):
                            player.money[activeItem.typing] += 1
                        else:
                            player.items.append(activeItem)
                        print('You bought the '+activeItemName+'!')
                        print()
                        input('Press enter to continue... ')
                        buySuccess = False
                    else:
                        print('You cannot afford that item.')
                        print()
                        input('Press enter to continue... ')
                        buySuccess = False
                else:
                    print('That item cannot be bought.')
                    print()
                    input('Press enter to continue...')
                    buySuccess = False
            elif buyRequestWords[0] == 'talk':
                #Work on this one
                pass

            elif buyRequestWords[0] == 'help':
                talkHelp(monster)
                buySuccess = False
            elif buyRequestWords[0] == 'sell':
                activeItemName = ' '.join(buyRequestWords[1:])
                activeItem = player.getItemByName(activeItemName)
                if activeItem in player.items:
                    monsterPay(player, monster, activeItem)
                    player.items.remove(activeItem)
                    monster.soldItems.append(activeItem)
                    print('You sold the '+activeItemName+'!')
                    print()
                    input('Press enter to continue... ')
                    buySuccess = False
                else:
                    print('That item cannot be sold.')
                    print()
                    input('Press enter to continue... ')
                    buySuccess = False
            else:
                print('That is not a valid command.')
                print()
                input('Press enter to continue... ')
                buySuccess = False
