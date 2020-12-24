def findDestination(currentCup, cups, pickedUp):
    targetNum = cups[currentCup] - 1
    while True:
        if targetNum < 1:
            targetNum = max(max(cups), max(pickedUp))
        if targetNum in pickedUp:
            targetNum -= 1
        else:
            return cups.index(targetNum)

def pickThree(cur, cups):
    debug = False

    pickTillEnd = cups[cur+1:cur+4]
    if debug: print(pickTillEnd)
    if cur + 3 >= len(cups):
        if debug: print('oh no')
        pickFromBegin = cups[:(cur + 4 - len(cups))]
        if debug: print(pickFromBegin)
    else:
        return pickTillEnd
    return pickTillEnd + pickFromBegin

def score(cups):
    start = cups.index(1)
    nums = cups[start+1:] + cups[:start]
    return ''.join(map(str, nums))

def moveCups(cups):
    debug = False
    cur = 0
    for i in range(100):
        if debug: print(f"Round #{i+1}: Starting cups: {cups}")
        curNum = cups[cur]
        if debug: print(f"Cur: {cur}, Cur value: {curNum}")
        pickedUp = pickThree(cur, cups)
        if debug: print(f"Picked up: {pickedUp}")
        for p in pickedUp: cups.remove(p)
        if debug: print(f"Cups after removing picked up: {cups}")
        destination = findDestination(cups.index(curNum), cups, pickedUp)
        if debug: print(f"Destination: {cups[destination]}")
        cups = cups[:destination+1] + pickedUp + cups[destination+1:]
        if debug: print(f"Cups at end of round: {cups}")
        cur = (cups.index(curNum) + 1) % (len(cups))
        if debug: print(f"New Cur {cups[cur]}")
        if debug: print()
    return score(cups)

with open('input.in', 'r') as f:
    cups = [int(c) for c in f.read().strip()]
    print(moveCups(cups))
