import numpy as np

def rideToboggan(trees, x, y):
    i, j, treesEncountered = 0, 0, 0
    while j < len(trees):
       treesEncountered += 1 if (trees[j][i]) == '#' else 0
       i = (i + x) % len(trees[0])
       j += y
    return treesEncountered

def checkAllSlopes(slopes, trees):
    return np.prod([rideToboggan(trees, s[0], s[1]) for s in slopes])

trees = [s.replace('\n', '') for s in open('day3.in', 'r').readlines()]
slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
print(f"Part 1: Number of trees: {checkAllSlopes([slopes[1]], trees)}")
print(f"Part 2: Number of trees: {checkAllSlopes(slopes, trees)}")
