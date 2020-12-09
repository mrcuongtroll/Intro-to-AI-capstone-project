import random

"""
East: e (increase cost by cost['e'])
West: w (decrease cost by cost['w'])
South: s (multiply cost by cost['s'])
North: n (divide cost by cost['n'])
Blocks: m x n
"""

m = int(input('m = '))
n = int(input('n = '))
sequence = input('Starting sequence (West: w, East: e, North: n, South: s): ').split()
cost = {}
cost['w'] = random.randint(2,4)
cost['e'] = random.randint(2,4)
cost['s'] = random.randint(2,4)
cost['n'] = random.randint(2,4)
oposite = {'w': 'e', 'e': 'w', 'n': 's', 's': 'n'}
print("Going East will increase the tax by", cost['e'])
print('Going West will decrease the tax by', cost['w'])
print('Going South will multiply the tax by', cost['s'])
print('Going North will divide the tax by', cost['n'])

class node():
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.available_dir = ['w', 'e', 's', 'n']
        self.tax = 0

TheMap = {}
for i in range(m+1):              #Initiate the map with nodes
    for j in range(n+1):
        TheMap[i,j] = node((i,j))
        if i == 0:
            TheMap[i,j].available_dir.remove('n')
        if i == m-1:
            TheMap[i,j].available_dir.remove('s')
        if j == 0:
            TheMap[i,j].available_dir.remove('w')
        if j == n-1:
            TheMap[i,j].available_dir.remove('e')
current = [0,0]                 #We start at the origin
current_tax = 0                 #Initial tax = 0

def GoEast():
    global current
    global TheMap
    global current_tax
    global sequence
    if 'e' not in TheMap[current[0], current[1]].available_dir:
        print('You cannot go east from here')
        return
    else:
        TheMap[current[0], current[1]].available_dir.remove('e')
        # sequence.append('e')
        current_tax += cost['e']
        current[0] += 1
        if 'w' in TheMap[current[0], current[1]].available_dir:
            TheMap[current[0], current[1]].available_dir.remove('w')
    return

def GoWest():
    global current
    global TheMap
    global current_tax
    global sequence
    if 'w' not in TheMap[current[0], current[1]].available_dir:
        print('You cannot go west from here')
        return
    else:
        TheMap[current[0], current[1]].available_dir.remove('w')
        # sequence.append('w')
        current_tax -= cost['w']
        current[0] -= 1
        if 'e' in TheMap[current[0], current[1]].available_dir:
            TheMap[current[0], current[1]].available_dir.remove('e')
    return

def GoSouth():
    global current
    global TheMap
    global current_tax
    global sequence
    if 's' not in TheMap[current[0], current[1]].available_dir:
        print('You cannot go south from here')
        return
    else:
        TheMap[current[0], current[1]].available_dir.remove('s')
        # sequence.append('s')
        current_tax *= cost['s']
        current[1] += 1
        if 'n' in TheMap[current[0], current[1]].available_dir:
            TheMap[current[0], current[1]].available_dir.remove('n')
    return

def GoNorth():
    global current
    global TheMap
    global current_tax
    global sequence
    if 'n' not in TheMap[current[0], current[1]].available_dir:
        print('You cannot go south from here')
        return
    else:
        TheMap[current[0], current[1]].available_dir.remove('n')
        # sequence.append('n')
        current_tax /= cost['n']
        current[1] -= 1
        if 's' in TheMap[current[0], current[1]].available_dir:
            TheMap[current[0], current[1]].available_dir.remove('s')
    return

for dir in sequence:
    if dir == 'w':
        GoWest()
    elif dir == 'e':
        GoEast()
    elif dir == 's':
        GoSouth()
    else:
        GoNorth()

print(sequence)
print(current)
print(current_tax)