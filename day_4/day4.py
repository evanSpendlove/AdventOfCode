def validatePassports(passports) -> int:
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    validPassports = 0
    for p in passports:
        p = {i.split(':')[0]:i.split(':')[1] for i in p}
        validPassports += all(p.get(f) for f in fields)

    return validPassports

with open('d4.in', 'r') as f:
    data = [
        i.replace('\n', ' ').split()
        for i in f.read().split('\n\n')
    ]
    print(f"Valid passports: {validatePassports(data)}")
