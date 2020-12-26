def findDestinationIdx(targetNum, pickedUp, n):
    for i in range(4):
        if targetNum < 1:
            targetNum = n
        if targetNum in pickedUp:
            targetNum -= 1
        else:
            return targetNum

def scoreP1(cups):
    return ''.join(map(str, cups[cups.index(1)+1:] + cups[:cups.index(1)]))

def scoreP2(cups):
    s = cups.index(1)
    return cups[(s+1) % len(cups)] * cups[(s+2) % len(cups)]

# Expensive operations:
# cups.index()
# cups = cups[] + p + cups[] --> changed to .insert()
# cups.remove()

def moveCups(cups, score):
    cur, n = 0, len(cups)
    for i in range(1000):
        curNum = cups[cur]
        pickedUp = cups[cur+1:cur+4]
        if cur + 3 >= n:
            pickedUp += cups[:(cur + 4 - n)]
        for p in pickedUp: cups.remove(p)
        destination = cups.index(findDestinationIdx(curNum - 1, pickedUp, n))
        for i in range(3):
            cups.insert(destination+1+i, pickedUp[i])
        cur = (cups.index(curNum) + 1) % (len(cups))
    return score(cups)

with open('input.in', 'r') as f:
    cups = [int(c) for c in f.read().strip()]
    # print(moveCups([c for c in cups], scoreP1))
    for i in range(len(cups)+1, 1000001): cups.append(i)
    print(moveCups(cups, scoreP2))
