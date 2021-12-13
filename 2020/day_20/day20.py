from collections import Counter
from numpy import prod

def rotate(tile):
    rotated = [list(row[:]) for row in tile]
    for i in range(len(tile)):
        for j in range(len(tile[0])):
                rotated[j][i] = tile[i][j]
    for i in range(len(rotated)):
        rotated[i] = ''.join(rotated[i])
    return flip(rotated)

def flip(tile):
    return [t[::-1] for t in tile]

# Matches the rightmost side of tileA to leftmost side of tileB
def matchSide(tileA, tileB):
    return all([
        tileA[i][-1] == tileB[i][0]
        for i in range(len(tileA))
        ])

# Matches bottom of tileA to top of tileB
def matchTop(tileA, tileB):
    return all([
        tileA[-1][i] == tileB[0][i]
        for i in range(len(tileA[-1]))
        ])

def findEdges(tile):
    return [
            tile[0],
            tile[-1][::-1],
            ''.join(row[-1] for row in tile),
            ''.join(row[0] for row in tile[::-1]),
            ]

def prodOfCorners(tiles):
    edges = Counter()
    for t in tiles.values():
        edges.update(findEdges(t))

    flippedEdges = Counter()
    for t in tiles.values():
        flippedEdges.update(findEdges(t[::-1]))

    edges += flippedEdges
    return prod([
        id for id, t in tiles.items()
        if sum([1 for e in findEdges(t) if edges[e] == 1]) == 2
        ])

with open('input.in', 'r') as f:
    images = f.read().strip().split('\n\n')
    tiles = {
                int(i.split('\n')[0][5:-1]): i.split('\n')[1:]
                for i in images
            }
    print(prodOfCorners(tiles))
