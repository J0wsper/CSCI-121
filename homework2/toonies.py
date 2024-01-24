price = int(input("Item cost in Canadian Dollars? "))
toonies = price//2 + price%2
print(str("Pay "+str(toonies)+" toonies."))