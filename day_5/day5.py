def binarySearch(boardingPass: str, low: int = 0, high: int = 127) -> int:
    for c in boardingPass:
        mid = low + (high - low) // 2
        if c in "FL":
           high = mid
        else:
            low = mid + 1
    return low

def parseBoardingpass(bpass):
    row = binarySearch(bpass[:7], high=127)
    col = binarySearch(bpass[7:], high=7)
    return row * 8 + col

with open('input.in', 'r') as f:
    highestID = max([parseBoardingpass(l.strip()) for l in f.readlines()])
    print(f"Highest ID: {highestID}")
