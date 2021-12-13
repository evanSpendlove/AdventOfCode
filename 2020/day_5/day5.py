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

def findMissingSeat(allSeats):
    # O(N*Log.N) solution
    allSeats.sort()
    for i in range(0, len(allSeats)-1):
        if allSeats[i] + 1 != allSeats[i+1]:
            return allSeats[i]+1
    return -1

def findMissingClever(allSeats):
    # O(N) solution
    # Explanation:
    #    We need to find the one missing value in this list.
    #    If we take the length of the list, N,  and sum all the values from 0 to
    #       N, then we have a target.
    #    Now, we can take the min and use it to rebase the values in the list
    #       from 0
    #    With that, we can sum all the values in the list, rebased from 0 and
    #       compare this against our actual target sum.
    #    We also need to remember to addd the first_seat back on to rebase it.
    targetSum = len(allSeats) * (len(allSeats) + 1) // 2
    firstSeat = min(allSeats)
    actualSum = sum([ID - firstSeat for ID in allSeats])
    return targetSum - actualSum + firstSeat

with open('input.in', 'r') as f:
    allSeats = [parseBoardingpass(l.strip()) for l in f.readlines()]
    print(f"Highest ID: {max(allSeats)}")
    print(f"Missing Seat ID: {findMissingClever(allSeats)}")

