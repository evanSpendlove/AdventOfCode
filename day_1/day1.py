def read_input(filename):
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
        lines = [int(l) for l in lines]
        return lines

def count_increases(data):
    counter = 0
    prev = data[0]
    for i in range(1, len(data)):
        counter += 1 if int(data[i] > prev) else 0
        prev = data[i]
    return counter

def compare_windows(w1, w2):
    return sum(w2) > sum(w1)

def sliding_increases(data):
    windows = []
    prev_window = [data[0], data[1], data[2]]
    for i in range(1, len(data) - 1):
        window = [data[i-1], data[i], data[i+1]]
        windows.append(sum(window))
    return count_increases(windows)

data = read_input('input.in')

count_1 = count_increases(data)
print(f"Part 1: Count = {count_1}")

count_2 = sliding_increases(data)
print(f"Part 2: Count = {count_2}")

