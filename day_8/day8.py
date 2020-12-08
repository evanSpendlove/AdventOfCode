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

def generateWinningStatesIter(program):
    winning = [None for i in range(len(program))]
    for i in range(len(program)):
        cycleResult = []
        lineIdx = i
        while len(cycleResult) is 0:
            if lineIdx >= len(program):
                cycleResult.append(1)
                break
            if winning[lineIdx] is not None:
                if len(winning[lineIdx]) is 0: 
                    winning[lineIdx] = cycleResult
                    cycleResult.append(-1)
                    break
                if len(winning[lineIdx]) > 0:
                    cycleResult.append(winning[lineIdx][0])
                    break
            winning[lineIdx] = cycleResult
            lineIdx = simulateLine(lineIdx, program)
    return winning


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
    winning_super_clever = generateWinningStatesIter(program)
    print(winning_super_clever)

    winning_dumb = [0 for i in range(len(program))]
    for i in range(len(program)):
        winning_dumb[i], _ = simulateCode(i, program)

    brokenCounter = 0
    for i in range(len(winning_dumb)):
        brokenCounter += 1 if winning_dumb[i] != winning_super_clever[i][0] else 0
        print(f"{winning_dumb[i]} == {winning_super_clever[i]}")
    print(f"verifyWinning.Broken Count: {brokenCounter}")

def computeWinningStates(program, winning, visited):
    for i in range(len(program)):
        generateWinningStates(i, program, winning, visited)

def fixProgramLinearSmart(program) -> int:
    start = current_milli_time()
    winning = generateWinningStatesIter(program)
    end = current_milli_time()
    print(f"ITER: Time taken to generate winning states: {end-start}")
    print(len(winning))

    start = current_milli_time()
    for i in range(len(program)):
        if "jmp" not in program[i] and "nop" not in program[i]:
            continue
        offset = 1 if "jmp" in program[i] else parseNumber(program[i])
        if i + offset >= len(winning):
            print("WTFFF" + str((i + offset)))
        if winning[i + offset][0] == 1:
            attempt = program.copy()
            if "jmp" in attempt[i]:
                attempt[i] = "nop" + attempt[i][3:]
            if "nop" in program[i]:
                attempt[i] = "jmp" + attempt[i][3:]
            success, result = simulateCode(0, attempt)
            if success is 1:
                end = current_milli_time()
                print(f"ITER: Time taken to fix program linear: {end-start}")
                return result


def fixProgramLinear(program) -> int:
    winning = [0 for i in range(len(program))]
    visited = [False for i in range(len(program))]
    start = current_milli_time()
    computeWinningStates(program, winning, visited)
    end = current_milli_time()
    print(f"Time taken to generate winning states: {end-start}")
    print(f"Length of winning {len(winning)}")

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
    verifyWinning(program)
    print(f"Program terminated with: {success}. The final value was: {result}")
    print(f"Program terminated with: 0. The final value was: {fixProgram(program)}")
    print(f"Program terminated with: 0. The final value was: {fixProgramLinear(program)}")
    print(f"Program terminated with: 0. The final value was: {fixProgramLinearSmart(program)}")

    speedTest = True
    if speedTest:
        bruteFunc = wrapper(fixProgram, program)
        optimalFunc = wrapper(fixProgramLinear, program)
        iterFunc = wrapper(fixProgramLinearSmart, program)
        bruteTime = timeit.timeit(bruteFunc, number=1)
        optimalTime = timeit.timeit(optimalFunc, number=1)
        iterTime = timeit.timeit(iterFunc, number=1)
        print(f"Time taken for brute force approach: {bruteTime}")
        print(f"Time taken for optimal approach: {optimalTime}")
        print(f"Time taken for iterative approach: {iterTime}")

