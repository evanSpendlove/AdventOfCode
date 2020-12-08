def parseNumber(line) -> int:
    sign = 1 if "+" in line else -1
    number = int(line[5:])
    return number * sign

def simulateCode(program) -> (int, int):
    lineIdx = 0
    lines = [0 for i in range(len(program))]
    globalCounter = 0
    while True:
        line = program[lineIdx].strip()
        if lineIdx >= len(program):
            return (0, globalCounter)
        if lines[lineIdx]:
            return (-1, globalCounter)
        lines[lineIdx] = 1

        if "nop" in line:
            lineIdx += 1
            continue
        elif "acc" in line:
            globalCounter += parseNumber(line)
            lineIdx += 1
        elif "jmp" in line:
            lineIdx += parseNumber(line)


with open('input.in', 'r') as f:
    lines = f.readlines()
    success, result = simulateCode(lines)
    print(f"Program terminated with: {success}. The final value was: {result}")
