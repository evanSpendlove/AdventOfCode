def cryptoShake(loopSize, subject):
    val = 1
    for i in range(loopSize):
        val *= subject
        val %= 20201227
    return val

def shakeHands(targetRem, subject):
    val, count = 1, 0
    while val != targetRem:
        val *= subject
        val %= 20201227
        count += 1
    return count

with open('input.in', 'r') as f:
    publicKeys = list(map(int, f.read().strip().split('\n')))
    print(publicKeys)
    loopSize = shakeHands(publicKeys[0], 7)
    encryptionKey = cryptoShake(loopSize, publicKeys[1])
    print(encryptionKey)

