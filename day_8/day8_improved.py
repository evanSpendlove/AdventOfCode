import timeit

# --------------------- SIMULATING PROGRAM EXECUTION ---------------------

def parseNumber(line) -> int:
    sign = 1 if "+" in line else -1
    number = int(line[5:])
    return number * sign

def simulateLine(i, program):
    line = program[i].strip()
    return i + 1 if "jmp" not in line else i + parseNumber(line)

def simulateInstruction(i, globalCounter, program):
    line = program[i].strip()
    i += 1 if "jmp" not in line else parseNumber(line)
    globalCounter += parseNumber(line) if "acc" in line else 0
    return i, globalCounter

def simulateCode(program) -> (int, int):
    i, accumulator = 0, 0
    visited = [0 for i in range(len(program))]
    while True:
        if i >= len(program):
            return (1, accumulator)
        if visited[i]:
            return (-1, accumulator)
        visited[i] = 1
        i, accumulator = simulateInstruction(i, accumulator, program)

# --------------------- COMPUTING EXITING STATES ---------------------

def computeExitingIterative(program):
    # I use a trick here to avoid having to update every value after
    # every cycle - using lists to have a mutable variable (reference).
    #    -> This simulates a pointer.
    #
    # By using lists as the cycleResult, I can make each instruction
    # visited reference the cycleResult of the cycle that it is part of.
    #
    # Then, when a cycle is complete, that cycleResult is updated and
    # all of the instructions in that cycle now hold that value.

    exiting = [None for i in range(len(program))]
    for i in range(len(program)):
        cycleResult = []
        lineIdx = i
        while len(cycleResult) is 0:
            if lineIdx >= len(program):
                cycleResult.append(1)
            elif exiting[lineIdx] is not None:
                # If visited and not previously computed, there is a cycle
                if len(exiting[lineIdx]) is 0:
                    exiting[lineIdx] = cycleResult
                    cycleResult.append(-1)
                # If visited and previously computed, use that value.
                elif len(exiting[lineIdx]) > 0:
                    cycleResult.append(exiting[lineIdx][0])
            else:
                exiting[lineIdx] = cycleResult
                lineIdx = simulateLine(lineIdx, program)
    return [i[0] for i in exiting]

def generateExitingRecursive(i, program, exiting, visited):
    if i >= len(program):
        return 1
    # If previously computed, return that value
    if exiting[i] != 0:
        return exiting[i]
    # If previously visited, cycle detected
    if visited[i]:
        exiting[i] = -1
        return -1
    visited[i] = True
    newIdx = simulateLine(i, program)
    exiting[i] = generateExitingRecursive(newIdx, program, exiting, visited)
    return exiting[i]

def computeExitingRecursive(program, exiting, visited):
    for i in range(len(program)):
        generateExitingRecursive(i, program, exiting, visited)

# --------------------- FIXING THE PROGRAM ---------------------

def verifyProgram(i, program):
    swap = {"jmp":"nop", "nop":"jmp"}
    attempt = program.copy()
    attempt[i] = swap[attempt[i][:3]] + attempt[i][3:]
    return simulateCode(attempt)

# Time Complexity: O(N^2)
def fixProgramBrute(program) -> int:
    swap = {"jmp":"nop", "nop":"jmp"}
    for i in range(len(program)):
        if program[i][0:3] not in swap:
            continue
        success, result = verifyProgram(i, program)
        if success is 1:
            return result

# Time Complexity: O(N)
def fixProgramLinear(exiting, program) -> int:
    swap = {"jmp":"nop", "nop":"jmp"}
    visited = [0 for i in range(len(program))]
    i = 0
    while True:
        if visited[i]:
            i += 1
            continue
        visited[i] = True
        if program[i][0:3] not in swap:
            continue
        offset = 1 if "jmp" in program[i] else parseNumber(program[i])
        if exiting[i + offset] == 1:
            success, result = verifyProgram(i, program)
            return result
        i = simulateLine(i, program)

def fixProgramIterative(program) -> int:
    return fixProgramLinear(computeExitingIterative(program), program)

def fixProgramRecursive(program) -> int:
    exiting = [0 for i in range(len(program))]
    visited = [False for i in range(len(program))]
    computeExitingRecursive(program, exiting, visited)
    return fixProgramLinear(exiting, program)

# --------------------- TIMING AND RUNNING VARIATIONS ---------------------

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

with open('input.in', 'r') as f:
    program = f.readlines()
    success, result = simulateCode(program)
    print(f"Program terminated with: {success}. The final value was: {result}")

    functions = [fixProgramBrute, fixProgramRecursive, fixProgramIterative]
    for f in functions: print(f"Program terminated with: 0. The final value was: {f(program)}")

    times = []
    approaches = ["brute force", "recursive", "iterative"]
    timeChange = lambda x, y: 100 *(1.0 - float(x)/float(y))
    for i in range(len(functions)):
        t = timeit.timeit(wrapper(functions[i], program), number=10) / 10.0
        times.append(t)
        print(f"Time taken for {approaches[i]} approach: {t}s")
        if i > 0:
            print(("Time improvement on previous best for %s: %.2f" % (approaches[i], timeChange(times[i], min(times[0:i])))) + "%")
        print()
