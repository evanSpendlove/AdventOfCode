import functools as ft

# ------------- Identifying Fields-------------
def removeInvalidTickets(tickets, rules):
    return [t for t in tickets if validateTicket(t, rules) == 0]

def identifyFields(tickets, rules):
    tickets = removeInvalidTickets(tickets, rules)
    ruleCounts = {r:[0 for i in range(len(rules.keys()))] for r in rules}
    for r, count in ruleCounts.items():
        for t in tickets:
            for idx, field in enumerate(t):
                if any([withinRange(field, i) for i in rules[r]]):
                    count[idx] += 1

    ruleCounts = {rule:[c - 190 for c in ruleCounts[rule]] for rule in ruleCounts.keys()}
    fields = ["" for i in range(len(rules))]
    for i in range(len(rules)):
        for rule, count in ruleCounts.items():
            if sum(count) == 1:
                position = count.index(1)
                fields[position] = rule
                for r in ruleCounts:
                    ruleCounts[r][position] = 0
    return fields

def productOfDepartures(myTicket, fields):
    vals = [myTicket[idx] for idx, f in enumerate(fields) if 'departure' in f]
    return ft.reduce(lambda x,y: x*y, vals)

# ------------- Validating Tickets -------------

def withinRange(field, i):
    return True if field >= i[0] and field <= i[1] else False

def isValidField(field, rules) -> int:
    return 0 if any([withinRange(field, interval) for rule in rules.values() for interval in rule]) else field

def validateTicket(ticket, rules):
    return sum([isValidField(field, rules) for field in ticket])

# ------------- Parsing Input -------------

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
    print(f"P1: Ticket scanning error rate: {sum(validateTicket(t, rules) for t in otherTickets)}")

    otherTickets.append(myTicket)
    fields = identifyFields(otherTickets, rules)
    print(f"P2: Magic number: {productOfDepartures(myTicket, fields)}")
