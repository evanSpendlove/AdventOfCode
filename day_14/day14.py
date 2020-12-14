def parseOp(op):
    address = int(op[op.index('[')+1:op.index(']')])
    value = int(op[op.index('=')+2:])
    return address, value

def runInitializer(operations):
    memory = {}
    mask = ""
    for op in operations:
        if "mask" in op:
            mask = op[op.index('=')+2:]
        if "mem" in op:
            address, value = parseOp(op)
            memory[address] = applyBitmask(mask, value)
    return sum(memory.values())


def applyBitmask(mask, value):
    binValue = list(f'{value:036b}')
    for i, bit in enumerate(mask):
        if bit == 'x': continue
        if bit == '1' or bit == '0': 
            binValue[i] = bit
    return int(''.join(binValue), 2)

with open('input.in', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    print(runInitializer(lines))
