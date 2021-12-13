from math import gcd
from functools import reduce

def waitTime(timestamp, busID):
    wait = (timestamp // busID) * busID
    if wait < timestamp:
        wait += busID
    return wait - timestamp, busID

def findFirstBus(timestamp, buses):
    return min([waitTime(timestamp, busID) for busID in buses])

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def processInput(lines):
    timestamp = int(lines[0].strip())
    return timestamp, [int(b) for b in lines[1].split(',') if b != 'x']

def sync(lines):
    buses = [int(bus) for bus in lines[1].replace('x', '0').split(",")]
    period, maxIdx = max((bus, i) for i, bus in enumerate(buses))
    remainders = [(i - maxIdx, bus) for i, bus in enumerate(buses) if bus]
    minRem = min(remainders)[0]
    time = 0
    while remainders:
        time += period
        synced = [bus for rem, bus in remainders if (time + rem) % bus == 0]
        if synced:
            period = reduce(lcm, [period] + synced)
            remainders = [(rem, bus) for rem, bus in remainders if bus not in synced]
    return time + minRem

with open('input.in', 'r') as f:
    lines = f.readlines()
    timestamp, buses = processInput(lines)
    wait, earliest = findFirstBus(timestamp, buses)
    print(f"P1: wait time = {wait * earliest}")
    print(f"P2: earliest timestamp = {sync(lines)}")
