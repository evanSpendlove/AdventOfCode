def countTrees(input, increment):
	x = 0.0
	flag = 0
	count = 0
	for line in input:
		if flag == 0:
			flag = 1
			continue
		x = incrementPosition(x, increment)
		if (x.is_integer() == True):
			if(line[int(x)] == '#'):
				count += 1
		else:
			continue
	return count

def incrementPosition(x, increment):
	x += increment
	x = x % 31
	return x

f = open('day3.in', 'r')
f1 = f.readlines()
slopes = [1,3,5,7,0.5]
sum = 1
for slope in slopes:
	curSum = countTrees(f1, slope)
	print(curSum)
	sum *= curSum

print(sum)
