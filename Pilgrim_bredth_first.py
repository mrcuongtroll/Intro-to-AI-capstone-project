import random
from collections import deque
import timeit

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


def ExpandNode(current: node):
    global thequeue
    if not current.available_dir:
        return
    tax = 0
    to_coordinates = ()
    action_sequence = ()
    for dir in current.available_dir:
        if dir == 'e':
            tax = current.tax + cost[dir]
            to_coordinates = (current.coordinates[0], current.coordinates[1] + 1)
            action_sequence = current.action_sequence + (dir,)
        elif dir == 'w':
            tax = current.tax - cost[dir]
            to_coordinates = (current.coordinates[0], current.coordinates[1] - 1)
            action_sequence = current.action_sequence + (dir,)
        elif dir == 's':
            tax = current.tax * cost[dir]
            to_coordinates = (current.coordinates[0] + 1, current.coordinates[1])
            action_sequence = current.action_sequence + (dir,)
        elif dir == 'n':
            tax = current.tax / cost[dir]
            to_coordinates = (current.coordinates[0] - 1, current.coordinates[1])
            action_sequence = current.action_sequence + (dir,)
        path = current.path + ({current.coordinates, to_coordinates},)
        toNode = node(coordinates=to_coordinates, path=path, tax=tax, action_sequence=action_sequence)
        thequeue.append(toNode)
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
            del current
        else:
            ExpandNode(current)
            del current
    print(best_tax)
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
    print("Going East will increase the tax by", cost['e'])
    print('Going West will decrease the tax by', cost['w'])
    print('Going South will multiply the tax by', cost['s'])
    print('Going North will divide the tax by', cost['n'])
    thequeue = deque()
    initial_tax = 0
    point = (0,0)
    next = ()
    initial_path = []
    for dir in initial_sequence:
        if dir == 'w':
            initial_tax -= cost[dir]
            next = (point[0], point[1]-1)
            initial_path.append({point,next})
        elif dir == 'e':
            initial_tax += cost[dir]
            next = (point[0], point[1] + 1)
            initial_path.append({point, next})
        elif dir == 's':
            initial_tax *= cost[dir]
            next = (point[0] + 1, point[1])
            initial_path.append({point, next})
        elif dir == 'n':
            initial_tax /= cost[dir]
            next = (point[0] - 1, point[1])
            initial_path.append({point, next})
        point = next
    thequeue.append(node(coordinates = point, tax = initial_tax, path = tuple(initial_path)))
    best_tax = 10e9
    best_action_sequence = ()
    t0 = timeit.default_timer()
    PilgrimBredthFirst()
    print("Time taken to solve this problem:", timeit.default_timer() - t0)
    best_path = [(0,0)]
    for movement in best_action_sequence:
        if movement == 'w':
            best_path.append((best_path[-1][0], best_path[-1][1] - 1))
        elif movement == 'e':
            best_path.append((best_path[-1][0], best_path[-1][1] + 1))
        elif movement == 'n':
            best_path.append((best_path[-1][0] - 1, best_path[-1][1]))
        elif movement == 's':
            best_path.append((best_path[-1][0] + 1, best_path[-1][1]))
