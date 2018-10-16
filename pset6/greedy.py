while True:
    change = float(input("O hai! How much change is owed?\n"))
    if change >= 0:
        break
    
cents = change * 100
coins = 0
    
coins += cents // 25
cents = cents % 25

coins += cents // 10
cents = cents % 10

coins += cents // 5
cents = cents % 5

print(int(coins + cents))