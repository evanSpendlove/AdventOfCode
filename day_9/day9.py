def isValidXMAS(i, nums):
    possibles = {(nums[i] - n) for n in nums[(i-25):i]}
    return any([nums[j] in possibles for j in range((i-25), i)])

def findInvalidXMAS(nums):
    idx = [not isValidXMAS(i, nums) for i in range(25, len(nums))].index(True) + 25
    return nums[idx]

def findXMASWeakness(target, nums):
    for i in range(len(nums)):
        curSum = nums[i]
        j = 1
        while curSum <= target and j < len(nums):
            curSum += nums[i + j]
            if curSum == target:
                return min(nums[i:i+j+1]) + max(nums[i:i+j+1])
            j += 1
    return -1

with open('input.in', 'r') as f:
    nums = [int(i) for i in f.readlines()]
    invalid = findInvalidXMAS(nums)
    print(f"P1: Invalid value: {invalid}")
    print(f"P2: XMAS Encrpytion Weakness: {findXMASWeakness(invalid, nums)}")
