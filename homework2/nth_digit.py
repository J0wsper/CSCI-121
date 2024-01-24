number = int(input("Enter a non-negative integer: "))
position = int(input("Enter a digit position: "))
digit = (number%(10**(position+1)))//10**position
print(str("The "+str(10**position)+"s digit of that integer is "+str(digit)+"."))