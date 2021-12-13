from copy import deepcopy

def parseTile(tile):
    directions = {
            "e":(1, 0), "w":(-1, 0),
            "ne":(1, 1), "nw":(0, 1),
            "se":(0, -1), "sw":(-1, -1)
            }
    i, x, y = 0, 0, 0
    while i < len(tile):
        d = tile[i]
        if d not in "ew": d += tile[i+1]
        i += len(d)
        dx, dy = directions[d]
        x, y = x+dx, y+dy
    return (x, y)

def flipTiles(tiles):
    flipped = set()
    for t in tiles:
        flip = parseTile(t)
        if flip in flipped:
            flipped.remove(flip)
        else:
            flipped.add(flip)
    return flipped

def neighbours(point):
    offsets = [(1, 0), (-1, 0), (1, 1), (0, 1), (0, -1), (-1, -1)]
    return [(tuple(map(sum, zip(point, o)))) for o in offsets]

def countNeighbours(flipped, point):
    return sum([1 for n in neighbours(point) if n in flipped])

def simulateArt(flipped):
    for i in range(100):
        basis = deepcopy(flipped)
        for t in basis:
            pointsToExplore = [t] + neighbours(t)
            for p in pointsToExplore:
                count = countNeighbours(basis, p)
                if count == 0 or count > 2 and p in basis and p in flipped:
                    flipped.remove(p)
                if count == 2 and p not in basis:
                    flipped.add(p)
    return len(flipped)

with open('input.in', 'r') as f:
    tiles = f.read().strip().split('\n')
    flipped = flipTiles(tiles)
    print(f"P1: {len(flipped)}")
    print(f"P2: {simulateArt(flipped)}")
