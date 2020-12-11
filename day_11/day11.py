def adjacentOcc(i, j, floorMap) -> int:
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    count = 0
    for idx in range(len(offsets)):
        dx, dy = offsets[idx]
        x, y = i + dx, j + dy
        if x >= 0 and x < len(floorMap) and y >= 0 and y < len(floorMap[0]):
            count += 1 if floorMap[x][y] == '#' else 0
    return count

def countSeats(floorMap) -> int:
    return sum([val == '#' for row in floorMap for val in row])

def simulateSeats(floorMap) -> int:
    newMap = [row[:] for row in floorMap]
    changed = False
    for i in range(len(floorMap)):
        for j in range(len(floorMap[0])):
            if floorMap[i][j] == 'L' and adjacentOcc(i, j, floorMap) == 0:
                newMap[i][j] = "#"
                changed = True
            if floorMap[i][j] == '#' and adjacentOcc(i, j, floorMap) >= 4:
                newMap[i][j] = "L"
                changed = True
    return newMap, changed

with open('input.in', 'r') as f:
    floorMap = [list(i) for i in f.readlines()]
    stableMap, changed = simulateSeats(floorMap)
    while changed:
        stableMap, changed = simulateSeats(stableMap)
    print(f"Changed: {changed}, Number of seats: {countSeats(stableMap)}")
