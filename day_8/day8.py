def parseNumber(line) -> int:
    sign = 1 if "+" in line else -1
    number = int(line[5:])
    return number * sign

def simulateCode(program) -> (int, int):
    lineIdx = 0
    lines = [0 for i in range(len(program))]
    globalCounter = 0
    while True:
        if lineIdx >= len(program):
            return (0, globalCounter)
        line = program[lineIdx].strip()
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

def fixProgram(program) -> int:
    for i in range(len(program)):
        attempt = program.copy()
        if "jmp" in attempt[i]:
            attempt[i] = "nop" + attempt[i][3:]
        if "nop" in program[i]:
            attempt[i] = "jmp" + attempt[i][3:]
        success, result = simulateCode(attempt)
        if success is 0:
            return result


with open('input.in', 'r') as f:
    program = f.readlines()
    success, result = simulateCode(program)
    print(f"Program terminated with: {success}. The final value was: {result}")
    result = fixProgram(program)
    print(f"Program terminated with: 0. The final value was: {result}")
