import re

def validatePassports(passports) -> (int, int):
    fields = {
            "byr": lambda x: 1920 <= int(x) <= 2002,
            "iyr": lambda x: 2010 <= int(x) <= 2020,
            "eyr": lambda x: 2020 <= int(x) <= 2030,
            "pid": lambda x: re.match(r'^[0-9]{9}$', x),
            "ecl": lambda x: re.match(r'^amb$|^blu$|^brn$|^gry$|^grn$|^hzl$|^oth$', x),
            "hcl": lambda x: re.match(r'#[a-f0-9]{6}$', x),
            "hgt": lambda x: ("cm" in x and (150 <= int(x.replace("cm", '')) <= 193)) or
                             ("in" in x and (59 <= int(x.replace("in", '')) <= 76))
    }

    validFields, validData = 0, 0
    for p in passports:
        p = {i.split(':')[0]:i.split(':')[1] for i in p}
        validFields += all(p.get(f) for f in fields.keys())
        validData += all(fields[f](p.get(f, "0")) and f in p for f in fields.keys())

    return (validFields, validData)

with open('d4.in', 'r') as f:
    data = [
        i.replace('\n', ' ').split()
        for i in f.read().split('\n\n')
    ]
    validFields, validData = validatePassports(data)
    print(f"Part 1: Passports with valid fields: {validFields}")
    print(f"Part 2: Passports with valid fields and data: {validData}")
