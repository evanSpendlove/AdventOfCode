def computeJoltDiff(adaptors) -> int:
    count = {1: 0, 3: 0}
    for i in range(1, len(adaptors)):
        count[adaptors[i] - adaptors[i-1]] += 1
    return count[1] * count[3]

def computeNumPaths(adaptors) -> int:
    n = len(adaptors)
    dp = [1] + [0] * (n-1)
    for i in range(n):
        for j in range(1, 4):
            if i + j < n and adaptors[i+j] <= adaptors[i] + 3:
                dp[i + j] += dp[i]
    return dp[-1]

with open('input.in', 'r') as f:
    adaptors = [0] + [int(i) for i in f.readlines()]
adaptors.sort()
adaptors.append(adaptors[-1] + 3)
print(f"The computed jolt diff is: {computeJoltDiff(adaptors)}")
print(f"The number of possible paths is: {computeNumPaths(adaptors)}")
