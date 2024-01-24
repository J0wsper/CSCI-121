x1 = float(input("Location x-coordinate? "))
y1 = float(input("Location y-coordinate? "))
x2 = float(input("Classroom x-coordinate? "))
y2 = float(input("Classroom y-coordinate? "))
d = ((x2 - x1)**2 + (y1 - y2)**2)**0.5
print("Distance:\n"+str(d))