price = int(input("Integer? "))
if price == 21:
    print("zap")
elif (price%7 == 0 or price%10==7 or (price//10 > 0 and (price//10)%7 == 0) or (price//100 > 0 and (price//100)%7 == 0)) and (price%3 == 0 or price%10==3 or (price//10 > 0 and (price//10)%3 == 0) or (price//100 > 0 and (price//10)%3 == 0)):
    print(str("zap buzz"))  
elif price%3 == 0 or price%10==3 or (price//10 > 0 and (price//10)%3 == 0) or (price//100 > 0 and (price//100)%3 == 0):
    print(str("buzz"))
elif price%7 == 0 or price%10==7 or (price//10 > 0 and (price//10)%7 == 0) or (price//100 > 0 and (price//100)%7 == 0):
    print(str("zap"))
else: 
    print(price)