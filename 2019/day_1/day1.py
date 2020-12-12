def calcFuel(mass) -> int:
    totalFuel = 0
    for m in mass:
        fuel = (m//3)-2
        totalFuel += fuel
        while fuel >= 0:
            fuel = (fuel//3)-2
            totalFuel += fuel if fuel > 0 else 0
    return totalFuel

with open('input.in', 'r') as f:
    lines = [int(i) for i in f.readlines()]
    fuel = sum([((x//3)-2) for x in lines])
    print(f"P1: Total fuel requirements: {fuel}")
    print(f"P2: Total fuel requirements: {calcFuel(lines)}")
