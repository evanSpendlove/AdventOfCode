rows = ['departure location', 'departure station', 'departure platform', 'departure track', 'departure date', 'departure time', 'arrival location', 'arrival station', 'arrival platform', 'arrival track', 'class', 'duration', 'price', 'route', 'row', 'seat', 'train', 'type', 'wagon', 'zone']
rows = [i for i in range(20)]
swaps = [(9, 2),(8,3),(7,4),(9,6),(13,7),(17,8),(15,9),(19,10),(16,11),(17,12),(19,13),(16,15),(17,16),(19,18)]
for i in range(len(swaps)):
    x, y = swaps[i]
    x -= 1
    y -= 1
    rows[x], rows[y] = rows[y], rows[x]
total = 1
fields = [157,101,107,179,181,163,191,109,97,103,89,113,167,127,151,53,83,61,59,173]
deps = []
print(rows)
print(fields)
#for i, r in enumerate(rows):
#    if 'departure' in r: 
#        total *= fields[i]
#        deps.append(fields[i])
#deps.sort()
print(deps)
print(total)

