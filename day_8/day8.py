import timeit
import time

current_milli_time = lambda: int(round(time.time() * 1000))

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def parseNumber(line) -> int:
    sign = 1 if "+" in line else -1
    number = int(line[5:])
    return number * sign

def simulateCode(start, program) -> (int, int):
    lineIdx = start
    lines = [0 for i in range(len(program))]
    globalCounter = 0
    while True:
        if lineIdx >= len(program):
            return (1, globalCounter)
        if lines[lineIdx]:
            return (-1, globalCounter)
        lines[lineIdx] = 1

        line = program[lineIdx].strip()

        if "jmp" in line:
            lineIdx += parseNumber(line)
            continue
        elif "acc" in line:
            globalCounter += parseNumber(line)
        lineIdx += 1

def fixProgram(program) -> int:
    start = current_milli_time()
    for i in range(len(program)):
        if "jmp" not in program[i] and "nop" not in program[i]:
            continue
        attempt = program.copy()
        if "jmp" in attempt[i]:
            attempt[i] = "nop" + attempt[i][3:]
        if "nop" in program[i]:
            attempt[i] = "jmp" + attempt[i][3:]
        success, result = simulateCode(0, attempt)
        if success is 1:
            end = current_milli_time()
            print(f"Time taken to fix program quadratic: {end-start}")
            return result

def simulateLine(lineIdx, program):
    line = program[lineIdx].strip()
    return lineIdx + 1 if "jmp" not in line else lineIdx + parseNumber(line)

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

def verifyWinning(program):
    winning_clever = [0 for i in range(len(program))]
    visited = [False for i in range(len(program))]
    computeWinningStates(program, winning_clever, visited)

    winning_dumb = [0 for i in range(len(program))]
    for i in range(len(program)):
        winning_dumb[i], _ = simulateCode(i, program)

    brokenCounter = 0
    for i in range(len(winning_dumb)):
        brokenCounter += 1 if winning_dumb[i] != winning_clever[i] else 0
    print(f"verifyWinning.Broken Count: {brokenCounter}")


def computeWinningStates(program, winning, visited):
    for i in range(len(program)):
        generateWinningStates(i, program, winning, visited)

def fixProgramLinear(program) -> int:
    winning = [0 for i in range(len(program))]
    visited = [False for i in range(len(program))]
    start = current_milli_time()
    computeWinningStates(program, winning, visited)
    end = current_milli_time()
    print(f"Time taken to generate winning states: {end-start}")

    start = current_milli_time()
    for i in range(len(program)):
        if "jmp" not in program[i] and "nop" not in program[i]:
            continue
        offset = 1 if "jmp" in program[i] else parseNumber(program[i])
        if winning[i + offset] == 1:
            attempt = program.copy()
            if "jmp" in attempt[i]:
                attempt[i] = "nop" + attempt[i][3:]
            if "nop" in program[i]:
                attempt[i] = "jmp" + attempt[i][3:]
            success, result = simulateCode(0, attempt)
            if success is 1:
                end = current_milli_time()
                print(f"Time taken to fix program linear: {end-start}")
                return result

with open('input.in', 'r') as f:
    program = f.readlines()
    success, result = simulateCode(0, program)
    print(f"Program terminated with: {success}. The final value was: {result}")
    print(f"Program terminated with: 0. The final value was: {fixProgram(program)}")
    print(f"Program terminated with: 0. The final value was: {fixProgramLinear(program)}")
    # verifyWinning(program)
   
    speedTest = True
    if speedTest:
        bruteFunc = wrapper(fixProgram, program)
        optimalFunc = wrapper(fixProgramLinear, program)
        bruteTime = timeit.timeit(bruteFunc, number=1)
        optimalTime = timeit.timeit(optimalFunc, number=1)
        print(f"Time taken for brute force approach: {bruteTime}")
        print(f"Time taken for optimal approach: {optimalTime}")

