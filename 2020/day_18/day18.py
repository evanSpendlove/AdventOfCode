import re

class num:
    def __init__(self, val):
        self.val = val
    def __mul__(self, other):
        return num(self.val * other.val)
    def __truediv__(self, other):
        return num(self.val * other.val)
    def __pow__(self, other):
        return num(self.val + other.val)

def evaluate(equation):
    v = re.sub(r'(\d+)', r'num(\1)', equation).replace('+','/')
    return eval(v).val

def evaluate2(equation):
    v = re.sub(r'(\d+)', r'num(\1)', equation).replace('+','**')
    return eval(v).val

with open('input.in', 'r') as f:
    equations = f.read().strip().split('\n')
    print(f"P1: {sum([evaluate(e) for e in equations])}")
    print(f"P2: {sum([evaluate2(e) for e in equations])}")
