import sympy

def rref(matrix, originalRows):
    N, M = len(matrix), len(matrix[0])
    i, j, k, c, m = 0, 0, 0, 0, 0
    flag = 0
    pro = 0.0

    for i in range(N):
        if matrix[i][i] == 0:
            c = 1
            while (i + c) < N and matrix[i+c][i] == 0:
                c += 1
            if (i+c) == N:
                flag = 1
                break
            j = i
            for k in range(N):
                matrix[j][k], matrix[j+c][k] = matrix[j+c][k], matrix[j][k]
                originalRows[j], originalRows[j+c] = originalRows[j+c], originalRows[j]
                print(j, j+c)
                print(originalRows)
        for j in range(N):
            if i != j:
                pro = matrix[j][i] / matrix[i][i]
                for k in range(N):
                    matrix[j][k] = matrix[j][k] - matrix[i][k] * pro

    return matrix, originalRows

# ------------- Identifying Fields-------------
def basicRREF(matrix):
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            matrix[r][c] -= 190

    for r in matrix:
        print(r)

    rows = [i for i in range(len(matrix))]
    reduced, newRows = rref(matrix, rows)
    print(reduced)
    print(newRows)
    print()
    print()
    print()

    for row in reduced:
        print(row)

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
    for r in ruleCounts:
        print(ruleCounts[r])
    countsList = list(ruleCounts.values())
    basicRREF([row[:] for row in countsList])

    for i, c in enumerate(countsList):
        countsList[i].append(i+1)
    print(countsList)
    matrix = sympy.Matrix(countsList)
    print(matrix.rref())

def sumDepartures(fields):
    return sum([fields[name] for name in fields if 'departure' in name])

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
    print(rules.keys())
    print(sum(validateTicket(t, rules) for t in otherTickets))
    otherTickets.append(myTicket)
    identifyFields(otherTickets, rules)
