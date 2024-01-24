price = int(input("Enter an integer: "))
price2 = int(input("Enter another integer: "))
if price == 0 and price2 == 0:
    print(str(price)+" is a multiple of "+str(price2)+".")
elif price2 == 0:
    print(str(price)+" is not a multiple of "+str(price2)+".")
elif price%price2 == 0:
    print(str(price)+" is a multiple of "+str(price2)+".")
else:
    print(str(price)+" is not a multiple of "+str(price2)+".")