def withinRange(field, i):
    return 1 if field >= i[0] and field <= i[1] else 0

def isValidField(field, rules) -> int:
    if any([withinRange(field, i) for interval in rules.values() for i in interval]):
        return 0
    else:
        return field

def validateTicket(ticket, rules):
    return sum([isValidField(field, rules) for field in ticket])

def parseRules(fields):
    rules = {}
    for f in fields.split('\n'):
        fieldName = f[:f.index(':')]
        firstRange = list(map(int, f[f.index(':')+2:f.index('or ')-1].split('-')))
        secondRange = list(map(int, f[f.index('or ')+3:].split('-')))
        rules[fieldName] = (firstRange, secondRange)
    return rules

def parseTicket(ticket):
    return list(map(int, ticket.split(',')))

def parseSections(sections):
    rules = parseRules(sections[0])
    myTicket = parseTicket(sections[1].split('\n')[1])
    otherTickets = [parseTicket(t) for t in sections[2].split('\n')[1:]]
    return rules, myTicket, otherTickets

with open('input.in', 'r') as f:
    sections = f.read().strip().split("\n\n")
    rules, myTicket, otherTickets = parseSections(sections)
    print(sum(validateTicket(t, rules) for t in otherTickets))
