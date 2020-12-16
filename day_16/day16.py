# RREF - should've transposed before doing RREF...

# ------------- Identifying Fields-------------
def basicRREF(matrix):
    # counts = list(ruleCounts.values())
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            matrix[r][c] -= 190

    for r in matrix:
        print(r)

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
    for _, count in ruleCounts.items():
        for c in range(len(count)):
            count[c] -= 190

    for r in ruleCounts:
        print(ruleCounts[r])

    fields = ["" for i in range(len(rules))]
    for i in range(len(rules)):
        for rule, count in ruleCounts.items():
            if sum(count) == 1:
                position = count.index(1)
                fields[position] = rule
                print(rule, position)
                for r in ruleCounts:
                    ruleCounts[r][position] = 0
    return fields
    # Rows = rules ;; Cols = tickets
    # counts = list(ruleCounts.values())
    # for r in range(len(counts)):
        # for c in range(len(counts[0])):
            # counts[r][c] -= 190
    # for r in counts:
        # print(r)
    # fields = {}
    # for row in range(len(counts)):
        # possibilities = sum([counts[row][col] for col in range(len(counts[0]))])
        # if possibilities == 1:
        # print(possibilities)

def productOfDepartures(myTicket, fields):
    prod = 1
    for idx, f in enumerate(fields):
        if 'departure' in f:
            prod *= myTicket[idx]
    return prod

# ------------- Validating Tickets -------------

def withinRange(field, i):
    return 1 if field >= i[0] and field <= i[1] else 0

def isValidField(field, rules) -> int:
    if any([withinRange(field, i) for interval in rules.values() for i in interval]):
        return 0
    else:
        return field

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
    print(sum(validateTicket(t, rules) for t in otherTickets))
    otherTickets.append(myTicket)
    fields = identifyFields(otherTickets, rules)
    print(productOfDepartures(myTicket, fields))
