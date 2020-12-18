def indexOfMatchingParens(equation):
    count = 0
    for i, c in enumerate(equation):
        if c == ')': count += 1
        if c == '(': count -= 1
        if count == 0: return i

def computeEquation(equation):
    calc = {'+':lambda x,y: x + y, '*': lambda x,y: x*y}
    if len(equation) == 1:
        return int(equation[0])
    if equation[0] == ')':
        end = indexOfMatchingParens(equation)
        arg1 =  computeEquation(equation[1:end])
        if len(equation[end:]) < 3:
            return arg1
        operator = equation[end + 2]
        arg2 = computeEquation(equation[end + 4:])
        return  calc[operator](arg1, arg2)
    else:
        arg1 = int(equation[0])
        operator = equation[2]
        return calc[operator](arg1, computeEquation(equation[4:]))

with open('input.in', 'r') as f:
    equations = [i[::-1] for i in f.read().strip().split('\n')]
    print(f"P1: Sum of results: {sum(list(map(computeEquation, equations)))}")
