import random
from collections import deque
import timeit

class state():
    def __init__(self, coordinates = (0,0), tax: float = 0, action_sequence = (), prev = ()):
        self.coordinates = coordinates
        self.tax = tax
        self.action_sequence = action_sequence
        self.prev = prev
    
class point():
    def __init__(self, coordinates = (0,0)):
        self.coordinates = coordinates
        self.available_dir = ['w', 'e', 's', 'n']
    def border(self):
        if self.coordinates[0] == 0:
            self.available_dir.remove('n')
        if self.coordinates[0] == m:
            self.available_dir.remove('s')
        if self.coordinates[1] == 0:
            self.available_dir.remove('w')
        if self.coordinates[1] == n:
            self.available_dir.remove('e')
        return



def ExpandNode(current: state):
    global queue
    if not map[current.coordinates].available_dir:
        return
    for dir in map[current.coordinates].available_dir:
        if dir == 'e':
            next_coordinates = (current.coordinates[0], current.coordinates[1] + 1)
            tax = current.tax + cost[dir]
            action_sequence = current.action_sequence + (dir,)
        elif dir == 'w':
            next_coordinates = (current.coordinates[0], current.coordinates[1] - 1)
            tax = current.tax - cost[dir]
            action_sequence = current.action_sequence + (dir,)
        elif dir == 's':
            next_coordinates = (current.coordinates[0] + 1, current.coordinates[1])
            tax = current.tax * cost[dir]
            action_sequence = current.action_sequence + (dir,)
        elif dir == 'n':
            next_coordinates = (current.coordinates[0] - 1, current.coordinates[1])
            tax = current.tax / cost[dir]
            action_sequence = current.action_sequence + (dir,)
        next_state = state(coordinates = next_coordinates, tax=tax, action_sequence=action_sequence, prev = current.coordinates)
        queue.append(next_state)
    return

def traverse(sequence):
    global map
    for i in range(m+1):
        for j in range(n+1):
            map[i,j].available_dir = ['w', 'e', 'n', 's']
            map[i,j].border()
    current = (0,0)
    for dir in sequence:
        map[current].available_dir.remove(dir)
        if dir == 'e':
            current = (current[0], current[1] + 1)
        elif dir == 'w':
            current = (current[0], current[1] - 1)
        elif dir == 's':
            current = (current[0] + 1, current[1])
        elif dir == 'n':
            current = (current[0] - 1, current[1])
        map[current].available_dir.remove(opposite[dir])

def close_off(node: tuple):
    #param: node: the coordinates of the node we are considering
    if node != (m,n) and len(map[node].available_dir) == 1:
        if map[node].available_dir[0] == 'e':
            next_to_check = (node[0], node[1] + 1)
            map[next_to_check].available_dir.remove('w')
        elif map[node].available_dir[0] == 'w':
            next_to_check = (node[0], node[1] - 1)
            map[next_to_check].available_dir.remove('e')
        elif map[node].available_dir[0] == 's':
            next_to_check = (node[0] + 1, node[1])
            map[next_to_check].available_dir.remove('n')
        elif map[node].available_dir[0] == 'n':
            next_to_check = (node[0] - 1, node[1])
            map[next_to_check].available_dir.remove('s')
        close_off(next_to_check)

def GoalTest(state: state):
    return state.coordinates == (m,n)

def Solution(state: state):
    global best_tax, best_action_sequence
    if state.tax < best_tax:
        best_tax = state.tax
        best_action_sequence = state.action_sequence
    return

def PilgrimBredthFirst():
    global queue
    while queue:
        current = queue.popleft()
        traverse(current.action_sequence)
        close_off(current.prev)
        if GoalTest(current):
            Solution(current)
        else:
            ExpandNode(current)
    print(best_tax)
    print(best_action_sequence)
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
    opposite = {'w':'e', 'e':'w', 's':'n', 'n':'s'}

    map = {}
    for i in range(m+1):
        for j in range(n+1):
            map[i,j] = point(coordinates = (i,j))
            map[i,j].border()

    queue = deque()
    initial_tax = 0
    initial_coordinates = (0,0)
    initial_prev = (0,0)
    for dir in initial_sequence:
        initial_prev = initial_coordinates
        if dir == 'w':
            initial_tax -= cost[dir]
            initial_coordinates = (initial_coordinates[0], initial_coordinates[1] - 1)
        elif dir == 'e':
            initial_tax += cost[dir]
            initial_coordinates = (initial_coordinates[0], initial_coordinates[1] + 1)
        elif dir == 's':
            initial_tax *= cost[dir]
            initial_coordinates = (initial_coordinates[0] + 1, initial_coordinates[1])
        elif dir == 'n':
            initial_tax /= cost[dir]
            initial_coordinates = (initial_coordinates[0] - 1, initial_coordinates[1])
    queue.append(state(coordinates = initial_coordinates, tax = initial_tax, action_sequence = tuple(initial_sequence), prev = initial_prev))
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
