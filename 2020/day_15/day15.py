def memoryGame(numbers, end) -> int:
    lastSpoken = {n: i+1 for i, n in enumerate(numbers[:-1])}
    num = numbers[-1]
    for turn in range(len(numbers), end):
        lastSpoken[num], num = turn, turn - lastSpoken.get(num, turn)
    return num

with open('input.in', 'r') as f:
    lines = [int(i) for i in f.read().strip().split(',')]
    print(memoryGame(lines, 2020))
    print(memoryGame(lines, 30000000))
