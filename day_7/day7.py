def parseBags(lines) -> dict:
    lines = [l.split(' contain ') for l in lines]
    bags = {}
    for line in lines:
        outer = line[0].replace('bags', '').strip()
        inner = {}
        if 'no other' not in line[1]:
            for bag in line[1].split(', '):
                colour = bag[bag.index(' ') + 1:bag.index(' bag')]
                number = int(bag[:bag.index(' ')])
                inner[colour] = number
        bags[outer] = inner
    return bags

def totalShiny(bags: dict) -> int:
    return sum([int(containsShiny(bags, colour)) for colour in bags])

def containsShiny(bags, colour) -> bool:
    for bag in bags[colour]:
        if bag == 'shiny gold' or containsShiny(bags, bag):
            return True
    return False

def countNestedBags(bags: dict, colour: str) -> int:
    return sum([v + v * countNestedBags(bags, k) for k, v in bags[colour].items()])

with open('input.in', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    bags = parseBags(lines)
    print(f"Total bags that can contain shiny golds: {totalShiny(bags)}")
    print("Total bags that contained by a shiny gold bag: " + str(countNestedBags(bags, "shiny gold")))
