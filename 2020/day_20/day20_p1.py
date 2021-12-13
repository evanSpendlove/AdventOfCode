from collections import Counter
from numpy import prod

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
