def processInstruction(opcode, arg1, arg2) -> int:
    if opcode == 1:
        return arg1 + arg2
    else:
        return arg1 * arg2

def runIntcode(ops):
    ip = 0 # Instruction pointer: Increments by 4
    while ip < len(ops):
        opcode = ops[ip]
        if opcode == 99:
            break
        arg1, arg2 = ops[ops[ip+1]], ops[ops[ip+2]]
        dest = ops[ip+3]
        ops[dest] = processInstruction(opcode, arg1, arg2)
        ip += 4
    return ops[0]

def runProgram(ops, val1, val2):
    ops_copy = ops.copy()
    ops_copy[1], ops_copy[2] = val1, val2
    return runIntcode(ops_copy)

def findTargetInput(ops, targetOutput):
    for i in range(100):
        for j in range(100):
            output = runProgram(ops, i, j)
            if output == targetOutput:
                return i, j
    return -1

with open('input.in', 'r') as f:
    lines = [int(c) for c in f.read().split(',')]
    noun, verb = findTargetInput(lines, 19690720)
    print(f"P1: output = {runProgram(lines, 12, 2)}")
    print(f"P2: target input = {100 * noun + verb}")
