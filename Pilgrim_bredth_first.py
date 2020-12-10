import random
from collections import deque

"""
East: e (increase cost by cost['e'])
West: w (decrease cost by cost['w'])
South: s (multiply cost by cost['s'])
North: n (divide cost by cost['n'])
Blocks: m x n
"""


class node():
    def __init__(self, coordinates = (0,0), path = (), tax: float = 0, action_sequence = ()):
        self.coordinates = coordinates
        self.available_dir = ['w', 'e', 's', 'n']
        self.path = path
        if self.coordinates[0] == 0 or {self.coordinates, (self.coordinates[0] - 1, self.coordinates[1])} in self.path:
            self.available_dir.remove('n')
        if self.coordinates[0] == m or {self.coordinates, (self.coordinates[0] + 1, self.coordinates[1])} in self.path:
            self.available_dir.remove('s')
        if self.coordinates[1] == 0 or {self.coordinates, (self.coordinates[0], self.coordinates[1] - 1)} in self.path:
            self.available_dir.remove('w')
        if self.coordinates[1] == n or {self.coordinates, (self.coordinates[0], self.coordinates[1] + 1)} in self.path:
            self.available_dir.remove('e')
        self.tax = tax
        self.action_sequence = action_sequence


def ExpandEast(dequeue = True, gothere = False):
    global thequeue, current
    if 'e' not in current.available_dir:
        print('You cannot go east from here')
        return
    else:
        current.available_dir.remove('e')
        tax = current.tax + cost['e']
        to_coordinates = (current.coordinates[0], current.coordinates[1] + 1)
        path = current.path + ({current.coordinates, to_coordinates},)
        if dequeue:
            action_sequence = current.action_sequence + ('e',)
        else:
            action_sequence = ()
        toNode = node(coordinates = to_coordinates, path = path, tax = tax, action_sequence= action_sequence)
        if 'w' in toNode.available_dir:
            toNode.available_dir.remove('w')
        if dequeue:
            thequeue.append(toNode)
        if gothere:
            current = toNode
    return

def ExpandWest(dequeue = True, gothere = False):
    global thequeue, current
    if 'w' not in current.available_dir:
        print('You cannot go West from here')
        return
    else:
        current.available_dir.remove('w')
        tax = current.tax - cost['w']
        to_coordinates = (current.coordinates[0], current.coordinates[1] - 1)
        path = current.path + ({current.coordinates, to_coordinates},)
        if dequeue:
            action_sequence = current.action_sequence + ('w',)
        else:
            action_sequence = ()
        toNode = node(coordinates = to_coordinates, path = path, tax = tax, action_sequence= action_sequence)
        if 'e' in toNode.available_dir:
            toNode.available_dir.remove('e')
        if dequeue:
            thequeue.append(toNode)
        if gothere:
            current = toNode
    return

def ExpandSouth(dequeue = True, gothere = False):
    global thequeue, current
    if 's' not in current.available_dir:
        print('You cannot go South from here')
        return
    else:
        current.available_dir.remove('s')
        tax = current.tax * cost['s']
        to_coordinates = (current.coordinates[0] + 1, current.coordinates[1])
        path = current.path + ({current.coordinates, to_coordinates},)
        if dequeue:
            action_sequence = current.action_sequence + ('s',)
        else:
            action_sequence = ()
        toNode = node(coordinates = to_coordinates, path = path, tax = tax, action_sequence= action_sequence)
        if 'n' in toNode.available_dir:
            toNode.available_dir.remove('n')
        if dequeue:
            thequeue.append(toNode)
        if gothere:
            current = toNode
    return

def ExpandNorth(dequeue = True, gothere = False):
    global thequeue, current
    if 'n' not in current.available_dir:
        print('You cannot go North from here')
        return
    else:
        current.available_dir.remove('n')
        tax = current.tax / cost['n']
        to_coordinates = (current.coordinates[0] - 1, current.coordinates[1])
        path = current.path + ({current.coordinates, to_coordinates},)
        if dequeue:
            action_sequence = current.action_sequence + ('n',)
        else:
            action_sequence = ()
        toNode = node(coordinates = to_coordinates, path = path, tax = tax, action_sequence= action_sequence)
        if 's' in toNode.available_dir:
            toNode.available_dir.remove('s')
        if dequeue:
            thequeue.append(toNode)
        if gothere:
            current = toNode
    return

def ExpandNode(node: node):
    while node.available_dir:
        if node.available_dir[0] == 'e':
            ExpandEast()
        elif node.available_dir[0] == 'w':
            ExpandWest()
        elif node.available_dir[0] == 's':
            ExpandSouth()
        elif node.available_dir[0] == 'n':
            ExpandNorth()
    return

def GoalTest():
    return current.coordinates == (m,n)

def Solution():
    global best_tax, best_action_sequence
    if current.tax < best_tax:
        best_tax = current.tax
        best_action_sequence = current.action_sequence
    return

def PilgrimBredthFirst():
    global thequeue, current
    while thequeue:
        current = thequeue.popleft()
        if GoalTest():
            Solution()
        elif not current.available_dir:
            continue
        else:
            ExpandNode(current)
    print("The optimal action sequence is:", best_action_sequence)
    print("which corresponds to the minimal tax:", best_tax)
    return

if __name__ == '__main__':
    m = int(input('m = '))
    n = int(input('n = '))
    initial_sequence = input('Starting action_sequence (West: w, East: e, North: n, South: s): ').split()
    random.seed(7)
    cost = {}
    cost['w'] = random.randint(2, 4)
    cost['e'] = random.randint(2, 4)
    cost['s'] = random.randint(2, 4)
    cost['n'] = random.randint(2, 4)
    oposite = {'w': 'e', 'e': 'w', 'n': 's', 's': 'n'}
    print("Going East will increase the tax by", cost['e'])
    print('Going West will decrease the tax by', cost['w'])
    print('Going South will multiply the tax by', cost['s'])
    print('Going North will divide the tax by', cost['n'])
    thequeue = deque()
    current = node()
    for dir in initial_sequence:
        if dir == 'w':
            ExpandWest(dequeue=False, gothere=True)
        elif dir == 'e':
            ExpandEast(dequeue=False, gothere=True)
        elif dir == 's':
            ExpandSouth(dequeue=False, gothere=True)
        else:
            ExpandNorth(dequeue=False, gothere=True)
    thequeue.append(current)
    best_tax = 10e9
    best_action_sequence = ()
    PilgrimBredthFirst()
