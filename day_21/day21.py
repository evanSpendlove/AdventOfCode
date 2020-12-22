from functools import reduce

def findNonAllergens(allergens):
    common = {a: reduce((lambda x, y: x&y), allergens[a]) for a in allergens}
    unsafe = {}
    while common:
        found = [(c,i) for c, i in common.items() if len(i) == 1]
        for f in found:
            unsafe[f[0]] = (list(f[1])[0])
            for c in common.keys():
                common[c] = common[c] - f[1]
            common = {c:i for c, i in common.items() if len(i)}
    return unsafe

def parseInput(lines):
    allergens, allIngredients = {}, set()
    for l in lines:
        ingredients, alls = l.split(' (contains ')
        ingredients = ingredients.strip().split(' ')
        allIngredients |= set(ingredients)
        alls = alls[:-1].replace(',','').split(' ')
        for a in alls:
            if a not in allergens:
                allergens[a] = []
            allergens[a].append(set(ingredients))
    return allergens, allIngredients

def countSafe(lines, ingreds):
    lines = [l.split(" (")[0].split(' ') for l in lines]
    return sum([len(set(l) & ingreds) for l in lines ])

with open('input.in', 'r') as f:
    lines = f.read().strip().split('\n')
    allergens, allIngredients = parseInput(lines)
    unsafe = findNonAllergens(allergens)
    allIngredients -= set(unsafe.values())
    canon = [unsafe[a] for a in sorted(unsafe.keys())]
    print(f"P1: Count of occurrences of safe ingredients: {countSafe(lines, allIngredients)}")
    print(f"P2: Canonical dangerous list: {','.join(canon)}")
