def parity(number):
    if number > 1:
        return('s')
    else:
        return('')

def price_bot(b):
    while len(b) <= 1:
        b = b+'0'
    return(str(b))

def toonie_bot(c,d):
    if c != 0 and d%2 == 0:
        t = (int(d+1)//2)
        return('Please give me '+str(t)+' toonie'+parity(t)+'. [hit RETURN]: ')
    elif c != 0 and d%2 != 0:
        t = int(d+1)//2
        return('Please give me '+str(t)+' toonie'+parity(t)+'. [hit RETURN]: ')
    elif c == 0 and d%2 == 0:
        t = d//2
        return('Please give me '+str(t)+' toonie'+parity(t)+'. [hit RETURN]: ')
    else:
        t = (d-1)//2
        return('Please give me '+str(t)+' toonie'+parity(t)+' and 1 loonie. [hit RETURN]: ')



barrier = str('|'*4)
print(barrier+(' '*10)+barrier)
print(barrier+' '*2+'_/TT\_'+' '*2+barrier)
print(barrier+' '*2+'\\\\||//'+' '*2+barrier)
print(barrier+' '*2+'\'-||-\''+' '*2+barrier)
print(barrier+(' '*10)+barrier)
print('Welcome to Canada!\n'+'-'*18+'\n')

c = int(input('Enter the current temperature in whole degrees Celsius: '))
f = c*1.8+32
f_i = int(f)
print('That means that it is '+str(f_i)+' degrees Fahrenheit outside.\n')
print("Let's get the cost of potato chips here in Canadian dollars and cents...")
chips_dollars = int(input("Enter the number of dollars per bag of chips: "))
chips_cents = int(input("Enter the number of cents per bag of chips: "))
chips_amount = int(input("Okay. Enter the number of bags would you like to purchase: "))
if chips_amount == 0:
    print('\nOkay! Thanks for chatting about our beautiful weather.')
else: 
    chips_flavor = str(input("Enter the chip flavor you prefer [plain, pickle, or ketchup]: "))
    if (chips_flavor != 'plain') and (chips_flavor != 'pickle') and (chips_flavor != 'ketchup'):
        print('Sounds tasty, but we can only offer you plain chips.\n')
        chips_flavor = 'plain'
    else:
        print()
    true_chips_dollars = (chips_dollars)*(chips_amount)+((chips_cents)*(chips_amount))//100
    true_chips_cents = ((chips_cents)*(chips_amount))%100
    print('Your total is $'+str(true_chips_dollars)+'.'+price_bot(str(true_chips_cents))+' Canadian.')
    if (true_chips_dollars+true_chips_cents) == 0:
        print('Enjoy your free '+chips_flavor+' chips!')
    else:
        print(toonie_bot(true_chips_cents,true_chips_dollars))
        str(input(''))
        print('Thank you! Here are your '+chips_flavor+' chips.')