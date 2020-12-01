def twoSum2020(nums, target: int) -> (int, int):
    remainders = set()
    for n in nums:
        remainder = target - n
        if remainder in remainders:
            return (n, remainder)
        if n not in remainders:
            remainders.add(n)
    return -1

def main():
    inputFile = open('input.txt', 'r')
    data = inputFile.readlines()
    nums = [int(d) for d in data]
    x, y = twoSum2020(nums, 2020)
    print(x * y)

    inputFile.close()

main()
