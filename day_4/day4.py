import re

def validatePassports(passports) -> (int, int):
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    validFields, validData = 0, 0
    for p in passports:
        p = {i.split(':')[0]:i.split(':')[1] for i in p}
        valid = all(p.get(f) for f in fields)
        validFields += 1 if valid else 0
        if valid:
            validData += 1 if validateData(p) is 1 else 0

    return (validFields, validData)

def validateData(passport) -> bool:
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    ret = 1
    for k, v in passport.items():
        if k == "hgt":
            if 'cm' in v:
                ret -= 1 if int(v[0:v.index('c')]) < 150 or int(v[0:v.index('c')]) > 193 else 0
            elif 'in' in v:
                ret -= 1 if int(v[0:v.index('i')]) < 59 or int(v[0:v.index('i')]) > 76 else 0
            else:
                ret -= 1
        elif k == "hcl":
            ret -= 1 if not re.match(r'^#[a-f0-9]{6}$', v) else 0
        elif k == "ecl":
            ret -= 1 if not re.match(r'^amb$|^blu$|^brn$|^gry$|^grn$|^hzl$|^oth$', v) else 0
        elif k == "pid":
            ret -= 1 if not re.match(r'^[0-9]{9}$', v)  else 0 
        elif k == "byr":
            ret -= 1 if int(v) < 1920 or  int(v) > 2002 else 0
        elif k == "iyr":
            ret -= 1 if int(v) < 2010 or int(v) > 2020 else 0
        elif k == "eyr":
            ret -= 1 if int(v) < 2020 or int(v) > 2030 else 0
    return ret

with open('d4.in', 'r') as f:
    data = [
        i.replace('\n', ' ').split()
        for i in f.read().split('\n\n')
    ]
    validFields, validData = validatePassports(data)
    print(f"Part 1: Valid fields: {validFields}")
    print(f"Part 2: Valid data: {validData}")
