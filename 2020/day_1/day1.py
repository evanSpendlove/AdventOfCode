def threeSum(nums, target) -> (int, int, int):
    nums.sort()
    for i in range(len(nums)-2):
        lower = i + 1
        upper = len(nums)-1
        while lower < upper:
            curSum = nums[lower] + nums[upper] + nums[i]
            if curSum == target:
                return (nums[lower], nums[i], nums[upper])
            elif curSum < target:
                lower += 1
            else:
                upper -= 1
    return (-1, -1, -1)

def twoSum2020(nums, target: int) -> (int, int):
    remainders = set()
    for n in nums:
        remainder = target - n
        if remainder in remainders:
            return (n, remainder)
        if n not in remainders:
            remainders.add(n)
    return (-1, -1)

inputFile = open('input.txt', 'r')
nums = [int(d) for d in inputFile.readlines()]
x, y = twoSum2020(nums, 2020)
print(f"Two sum product: {x * y}")
x, y, z = threeSum(nums, 2020)
print(f"Three sum product: {x * y * z}")
inputFile.close()
