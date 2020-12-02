def validatePasswords(pwds) -> int:
    validPwds = 0

    for line in pwds:
        data = line.split(' ')
        sep = data[0].index('-')
        low = int(data[0][0:sep])
        high = int(data[0][sep+1:])

        targetChar = data[1][0]
        count = 0
        password = data[2]
        for _, c in enumerate(password):
            count += 1 if c == targetChar else 0
        validPwds += 1 if count >= low and count <= high else 0

    return validPwds

def validateNewPolicy(pwds) -> int:
    validPwds = 0

    for line in pwds:
        data = line.split(' ')
        sep = data[0].index('-')
        low = int(data[0][0:sep]) - 1
        high = int(data[0][sep+1:]) - 1
        targetChar = data[1][0]
        count = 0
        password = data[2]
        
        count += 1 if password[low] == targetChar else 0
        if len(password) > high:
            count += 1 if password[high] == targetChar else 0

        validPwds += 1 if count == 1 else 0 

    return validPwds

pwds = open('input.txt', 'r')
print(f"Valid Passwords count: {validateNewPolicy(pwds)}")
