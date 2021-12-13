import re

def buildRegex(rules, r):
    if rules[r][0] in "ab":
        return rules[r][0]

    rx = "("
    for subRule in rules[r]:
        if subRule == "|":
            rx += subRule
        else:
            rx += buildRegex(rules, subRule)
    return rx + ")"

def part1(rules, words):
    r1 = f"^{buildRegex(rules, '0')}$"
    return sum([int((re.match(r1, w) is not None)) for w in words])

def part2(rules, words):
    rule42 = buildRegex(rules, '42')
    rule31 = buildRegex(rules, '31')

    counter = 0
    for n in range(1, 6):
        r2 = f"^({rule42}+{rule42}{{{n}}}{rule31}{{{n}}})$"
        for w in words:
            counter += int((re.match(r2, w) is not None))
    return counter


def parseRules(data):
    rules = {}
    for d in data:
        delimiter = d.index(':')
        num = d[:delimiter]
        rule = d[delimiter+2:]
        rules[num] = rule.replace('"', '').split(' ')
    return rules

with open('input.in', 'r') as f:
    sections = [l.split('\n') for l in f.read().strip().split('\n\n')]
    rules, words = parseRules(sections[0]), sections[1]
    print(f"P1: total valid words: {part1(rules, words)}")
    print(f"P2: total valid words: {part2(rules, words)}")
