def parseInstruction(direction, instruction):
    actions = {'N':(1, 0), 'S':(-1, 0), 'E':(0, 1), 'W':(0, -1)}
    rotations = {'N':'E', 'E':'S', 'S':'W', 'W':'N'}
    act, val = instruction
    if act == 'F':
        change = [ch * val for ch in actions[direction]]
        return change[0], change[1], direction
    if act in actions:
        change = [ch * val for ch in actions[act]]
        return change[0], change[1], direction
    if act in ['L', 'R']:
        rots = (360-val)//90 if act == 'L' else val // 90
        for i in range(rots): direction = rotations[direction]
        return 0, 0, direction

def parseRelativeInstruction(ship_dir, wp_dir, wp_i, wp_j, instruction):
    actions = {'N':(1, 0), 'S':(-1, 0), 'E':(0, 1), 'W':(0, -1)}
    rotations = {'N':'E', 'E':'S', 'S':'W', 'W':'N'}
    act, val = instruction
    if act == 'F':
        return wp_i * val, wp_j * val, ship_dir
    if act in actions:
        change = [ch * val for ch in actions[act]]
        return (change[0] + wp_i), (change[1] + wp_j), wp_dir
    if act in ['L', 'R']:
        rots = (360-val)//90 if act == 'L' else val // 90
        for i in range(rots):
            wp_i, wp_j = -wp_j, wp_i
            wp_dir = rotations[wp_dir]
        return wp_i, wp_j, wp_dir


def navigateSea(instructions):
    i, j, direction = 0, 0, 'E'
    for instruction in instructions:
        di, dj, direction = parseInstruction(direction, instruction)
        i, j = i + di, j + dj
    return abs(i) + abs(j)

def navigateWithWaypoint(instructions):
    ship_i, ship_j, ship_dir = 0, 0, 'E'
    wp_i, wp_j, wp_dir= 1, 10, 'E'
    for instruction in instructions:
        di, dj, new_dir = parseRelativeInstruction(ship_dir, wp_dir, wp_i, wp_j, instruction)
        if 'F' in instruction:
            ship_i, ship_j = ship_i + di, ship_j + dj
        else:
            wp_i, wp_j, wp_dir = di, dj, new_dir
    return abs(ship_i) + abs(ship_j)

with open('input.in', 'r') as f:
    lines = [(line[0], int(line[1:])) for line in f.readlines()]
    print(f"P1: Manhattan distance after navigation: {navigateSea(lines)}")
    print(f"P2: Manhattan distance after waypoint navigation: {navigateWithWaypoint(lines)}")
