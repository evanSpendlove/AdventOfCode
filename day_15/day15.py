def memoryGame(nums, end) -> int:
    lastSpoken = {num: i for i, num in enumerate(nums[:-1])}
    curNum = nums[-1]
    for turn in range(len(nums), end):
        prevNum = curNum
        curNum = turn - lastSpoken.get(curNum, turn-1) - 1
        lastSpoken[prevNum] = turn - 1
    return curNum


with open('input.in', 'r') as f:
    lines = [int(i) for i in f.read().strip().split(',')]
    tests = [
                [0, 3, 6],
                [1, 3, 2],
                [2, 1, 3],
                [1, 2, 3],
                [2, 3, 1],
                [3, 2, 1],
                [3, 1, 2]
            ]
    outputs = [436, 1, 10, 27, 78, 438, 1836]
    for i, t in enumerate(tests):
        assert(outputs[i] == memoryGame(t, 2020))
    print(memoryGame(lines, 2020))
    print(memoryGame(lines, 30000000))
