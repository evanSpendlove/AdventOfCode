from itertools import product
from collections import Counter

def parseInput(data, dim):
    active = set()
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == '#':
                active.add(tuple([i,j] + [0] * (dim-2)))
    return active

def simulate(active, dim):
    c = Counter()
    for point in active:
        for offset in product([-1, 0, 1], repeat=dim):
            new = tuple(map(sum, zip(point, offset)))
            if new != point:
                c[new] += 1
    keep_on = set([point for point in active if c[point] in [2,3]])
    turn_on = set([point for point, neighbours in c.items() if point not in active and neighbours == 3])
    return keep_on | turn_on

def iterateSimulation(dim, data, n):
    active = parseInput(data, dim)
    for _ in range(n):
        active = simulate(active, dim)
    return len(active)

with open('input.in', 'r') as f:
    lines = f.read().strip().split('\n')
    dim = [3, 4]
    for d in dim:
        print(f"Part {dim.index(d) + 1}: {iterateSimulation(d, lines, 6)}")
