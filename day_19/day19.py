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
    rules[8] = "42 | 42 8".split(' ')
    rules[11] = "42 31 | 42 11 31".split(' ')
    r2 = f"^{buildRegex(rules, '0')}$"
    return sum([int((re.match(r2, w) is not None)) for w in words])


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

