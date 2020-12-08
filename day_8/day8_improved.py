import timeit
import time

# --------------------- SIMULATING PROGRAM EXECUTION ---------------------

def parseNumber(line) -> int:
    sign = 1 if "+" in line else -1
    number = int(line[5:])
    return number * sign

def simulateLine(idx, program):
    line = program[idx].strip()
    return idx + 1 if "jmp" not in line else idx + parseNumber(line)

def simulateInstruction(idx, globalCounter, program):
    line = program[idx].strip()
    idx += 1 if "jmp" not in line else parseNumber(line)
    globalCounter += parseNumber(line) if "acc" in line else 0
    return idx, globalCounter

def simulateCode(program) -> (int, int):
    idx = 0
    visited = [0 for i in range(len(program))]
    accumulator = 0
    while True:
        if idx >= len(program):
            return (1, accumulator)
        if visited[idx]:
            return (-1, accumulator)
        visited[idx] = 1
        idx, accumulator = simulateInstruction(idx, accumulator, program)

# --------------------- COMPUTING EXITING STATES ---------------------

def computeExitingIterative(program):
    exiting = [None for i in range(len(program))]
    for i in range(len(program)):
        cycleResult = []
        lineIdx = i
        while len(cycleResult) is 0:
            if lineIdx >= len(program):
                cycleResult.append(1)
                break
            if exiting[lineIdx] is not None:
                if len(exiting[lineIdx]) is 0:
                    exiting[lineIdx] = cycleResult
                    cycleResult.append(-1)
                    break
                if len(exiting[lineIdx]) > 0:
                    cycleResult.append(exiting[lineIdx][0])
                    break
            exiting[lineIdx] = cycleResult
            lineIdx = simulateLine(lineIdx, program)
    return [i[0] for i in exiting]

def generateWinningStates(lineIdx, program, winning, visited):
    if lineIdx >= len(program):
        return 1
    if winning[lineIdx] != 0:
        return winning[lineIdx]
    if visited[lineIdx]:
        winning[lineIdx] = -1
        return -1
    visited[lineIdx] = True
    newIdx = simulateLine(lineIdx, program)
    val = generateWinningStates(newIdx, program, winning, visited)
    winning[lineIdx] = val
    return val

def computeWinningStates(program, winning, visited):
    for i in range(len(program)):
        generateWinningStates(i, program, winning, visited)

# --------------------- FIXING THE PROGRAM ---------------------

def fixProgram(program) -> int:
    swap = {"jmp":"nop", "nop":"jmp"}
    attemptCounter = 0
    for i in range(len(program)):
        instruction = program[i][0:3]
        if instruction not in swap:
            continue
        attempt = program.copy()
        attempt[i] = swap[instruction] + attempt[i][3:]
        success, result = simulateCode(attempt)
        attemptCounter += 1
        if success is 1:
            print(f"Instruction #{i}, Attempt#{attemptCounter}")
            return result

# TODO: Refactor winning to exiting

def fixProgramLinear2(winning, program) -> int:
    swap = {"jmp":"nop", "nop":"jmp"}
    lines = [0 for i in range(len(program))]
    i = 0
    while True:
        if lines[i]:
            i += 1
            continue
        lines[i] = True
        instruction = program[i][0:3]
        if instruction not in swap:
            continue
        offset = 1 if "jmp" in program[i] else parseNumber(program[i])
        if winning[i + offset] == 1:
            attempt = program.copy()
            attempt[i] = swap[instruction] + attempt[i][3:]
            success, result = simulateCode(attempt)
            return result
            if success is 1:
                return result
        i = simulateLine(i, program)

def fixProgramLinear(winning, program) -> int:
    swap = {"jmp":"nop", "nop":"jmp"}
    for i in range(len(program)-2, -1, -1):
        instruction = program[i][0:3]
        if instruction not in swap:
            continue
        offset = 1 if "jmp" in program[i] else parseNumber(program[i])
        if winning[i + offset] == 1:
            attempt = program.copy()
            attempt[i] = swap[instruction] + attempt[i][3:]
            success, result = simulateCode(attempt)
            if success is 1:
                return result

def fixProgramIterative(program) -> int:
    return fixProgramLinear(computeExitingIterative(program), program)

def fixProgramRecursive(program) -> int:
    winning = [0 for i in range(len(program))]
    visited = [False for i in range(len(program))]
    computeWinningStates(program, winning, visited)
    return fixProgramLinear(winning, program)

def fixProgramTest(program) -> int:
    return fixProgramLinear2(computeExitingIterative(program), program)

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

with open('input.in', 'r') as f:
    program = f.readlines()
    success, result = simulateCode(program)
    print(f"Program terminated with: {success}. The final value was: {result}")

    functions = [fixProgram, fixProgramRecursive, fixProgramIterative, fixProgramTest]
    for f in functions:
        print(f"Program terminated with: 0. The final value was: {f(program)}")

    speedTest = True
    if speedTest:
        times = []
        approaches = ["brute force", "recursive", "iterative", "improved iterative"]
        for i in range(len(functions)):
            t = timeit.timeit(wrapper(functions[i], program), number=10) / 10.0
            times.append(t)
            print(f"Time taken for {approaches[i]} approach: {t}")

        timeImprovement = lambda x, y: 1.0 - float(x)/float(y)

        for i in range(1, len(times)):
            print(f"Time improvement for {approaches[i]}: {timeImprovement(times[i], min(times[0:i]))}")
