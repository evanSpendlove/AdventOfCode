def waitTime(timestamp, busID):
    wait = (timestamp // busID) * busID
    if wait < timestamp:
        wait += busID
    return wait - timestamp, busID

def findFirstBus(timestamp, buses):
    return min([waitTime(timestamp, busID) for busID in buses])

def processInput(lines):
    timestamp = int(lines[0].strip())
    buses = []
    for l in lines[1].split(','):
        if l != 'x':
            buses.append(int(l))
    return timestamp, buses


with open('input.in', 'r') as f:
    lines = f.readlines()
    timestamp, buses = processInput(lines)
    wait, earliest = findFirstBus(timestamp, buses)
    print(f"P1: time = {wait * earliest}")
