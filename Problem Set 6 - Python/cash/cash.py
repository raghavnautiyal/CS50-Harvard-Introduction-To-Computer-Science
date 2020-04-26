from cs50 import get_float

fint = 0
coins = 0

penny = 1
nickel = 5
dime = 10
quarter = 25

# get a float from the user
f = get_float("Change owed: ")
f = round(f * 100)

# keep subtracting a number till you cannot subtract it anymore, then move on to a smaller value
while f < 0:
    f = get_float("Change owed: ")
    f = round(f * 100)

while f - quarter >= 0:
    f = f - quarter
    coins += 1

while f - dime >= 0:
    f = f - dime
    coins += 1

while f - nickel >= 0:
    f = f - nickel
    coins += 1

while f - penny >= 0:
    f = f - penny
    coins += 1

# print the number of coins required
print(coins)