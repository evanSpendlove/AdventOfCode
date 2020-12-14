def parseOp(op):
    address = int(op[op.index('[')+1:op.index(']')])
    value = int(op[op.index('=')+2:])
    return address, value

def applyBitwiseAND(mask, value):
    binValue = list(f'{value:036b}')
    for i, bit in enumerate(mask):
        if bit == '1' or bit == '0': 
            binValue[i] = bit
    return int(''.join(binValue), 2)

def runInitializer(operations):
    memory = {}
    mask = ""
    for op in operations:
        if "mask" in op:
            mask = op[op.index('=')+2:]
        if "mem" in op:
            address, value = parseOp(op)
            memory[address] = applyBitwiseAND(mask, value)
    return sum(memory.values())

def applyBitwiseOR(mask, value):
    floatingValues = [list(f'{value:036b}')]
    binaryValues = []

    # Initial run over number
    for i, bit in enumerate(mask):
        if bit == '1':
            floatingValues[0][i] = '1'
        if bit == 'X':
            floatingValues[0][i] = 'X'

    while floatingValues:
        binVal = floatingValues.pop()
        # Find the first X.
        firstX = binVal.index('X')
        # Make a version with a 0 and with a 1
        versions = [binVal.copy(), binVal.copy()]
        for i in range(len(versions)):
            versions[i][firstX] = str(i)
        # Add to floatingValues if X in version, else add to binaryValues
            if 'X' in versions[i]:
                floatingValues.append(versions[i])
            else:
                #print(versions[i])
                binaryValues.append(int(''.join(versions[i]), 2))
    return binaryValues

def runInitializerV2(operations):
    memory = {}
    mask = ""
    for op in operations:
        if "mask" in op:
            mask = op[op.index('=')+2:]
        if "mem" in op:
            address, value = parseOp(op)
            addresses = applyBitwiseOR(mask, address)
            for addr in addresses:
                memory[addr] = value
    return sum(memory.values())

with open('input.in', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    print(f"P1: sum of memory: {runInitializer(lines)}")
    print(f"P2: sum of memory (V2): {runInitializerV2(lines)}")
