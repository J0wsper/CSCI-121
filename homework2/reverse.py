number = int(input("Enter a 3-digit integer: "))
reverse = (number%10)*100+((number%100)//10)*10+(number//100)
print(reverse)