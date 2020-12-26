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
    return len(flipped)

with open('input.in', 'r') as f:
    tiles = f.read().strip().split('\n')
    print(flipTiles(tiles))
