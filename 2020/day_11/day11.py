def countAdj(i, j, floorMap) -> int:
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    count = 0
    for idx in range(len(offsets)):
        dx, dy = offsets[idx]
        x, y = i + dx, j + dy
        if x >= 0 and x < len(floorMap) and y >= 0 and y < len(floorMap[0]):
            count += 1 if floorMap[x][y] == '#' else 0
    return count

def advancedAdj(i, j, floorMap) -> int:
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    count = 0
    for idx in range(len(offsets)):
        found = False
        dx, dy = offsets[idx]
        x, y = i + dx, j + dy
        while not found and (x >= 0 and x < len(floorMap)) and (y >= 0 and y < len(floorMap[0])):
            found = floorMap[x][y] != '.'
            count += 1 if floorMap[x][y] == '#' and found else 0
            x, y = x + dx, y + dy
    return count

def countSeats(floorMap) -> int:
    return sum([val == '#' for row in floorMap for val in row])

def simulateSeats(floorMap, adjFunc, upperLimit) -> bool:
    newMap = [row[:] for row in floorMap]
    changed = False
    for i in range(len(floorMap)):
        for j in range(len(floorMap[0])):
            if floorMap[i][j] == 'L' and adjFunc(i, j, floorMap) == 0:
                newMap[i][j] = "#"
                changed = True
            if floorMap[i][j] == '#' and adjFunc(i, j, floorMap) >= upperLimit:
                newMap[i][j] = "L"
                changed = True
    return newMap, changed

with open('input.in', 'r') as f:
    floorMap = [list(i.strip()) for i in f.readlines()]
    parts = [[countAdj, 4], [advancedAdj, 5]]
    for p in parts:
        seats, changed = simulateSeats(floorMap, p[0], p[1])
        while changed: seats, changed = simulateSeats(seats, p[0], p[1])
        print(f"P{parts.index(p)+1}: Number of seats: {countSeats(seats)}")
