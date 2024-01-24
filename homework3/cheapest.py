def cheapest(boxes):
    if boxes%14 > 0:
        bob_overflow = 1
    else:
        bob_overflow = 0
    if boxes%11 > 0:
        alice_overflow = 1
    else:
        alice_overflow = 0
    if ((boxes//14)+bob_overflow)*250 < ((boxes//11)+alice_overflow)*200:
        return('Bob')
    else:
        return('Alice')