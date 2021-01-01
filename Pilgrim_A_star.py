import random
import timeit
import heapq
from dataclasses import dataclass, field
from typing import Any
import numpy as np
import math


"""
East: e (increase cost by cost['e'])
West: w (decrease cost by cost['w'])
South: s (multiply cost by cost['s'])
North: n (divide cost by cost['n'])
Blocks: m x n
"""

# @dataclass(order=True)
# class node():
#     def __init__(self, coordinates = (0,0), path = (), tax: float = 0, estimate: float = 0, action_sequence = (), lines = 0):
#         self.coordinates = coordinates
#         self.available_dir = ['w', 'e', 's', 'n']
#         self.path = path
#         if self.coordinates[0] == 0 or {self.coordinates, (self.coordinates[0] - 1, self.coordinates[1])} in self.path:
#             self.available_dir.remove('n')
#         if self.coordinates[0] == m or {self.coordinates, (self.coordinates[0] + 1, self.coordinates[1])} in self.path:
#             self.available_dir.remove('s')
#         if self.coordinates[1] == 0 or {self.coordinates, (self.coordinates[0], self.coordinates[1] - 1)} in self.path:
#             self.available_dir.remove('w')
#         if self.coordinates[1] == n or {self.coordinates, (self.coordinates[0], self.coordinates[1] + 1)} in self.path:
#             self.available_dir.remove('e')
#         self.tax = tax
#         self.action_sequence = action_sequence
#         self.priority = tax
#         self.item: Any = field(compare=False)
#     priority: float
    # item: Any

class node():
    def __init__(self, coordinates = (0,0), path = (), tax: float = 0, action_sequence = ()):
        self.coordinates = coordinates
        self.available_dir = ['w', 'e', 's', 'n']
        self.path = path
        if self.coordinates[0] == 0 or {self.coordinates, (self.coordinates[0] - 1, self.coordinates[1])} in self.path:
            self.available_dir.remove('n')
        if self.coordinates[0] == m-1 or {self.coordinates, (self.coordinates[0] + 1, self.coordinates[1])} in self.path:
            self.available_dir.remove('s')
        if self.coordinates[1] == 0 or {self.coordinates, (self.coordinates[0], self.coordinates[1] - 1)} in self.path:
            self.available_dir.remove('w')
        if self.coordinates[1] == n-1 or {self.coordinates, (self.coordinates[0], self.coordinates[1] + 1)} in self.path:
            self.available_dir.remove('e')
        self.tax = tax
        self.action_sequence = action_sequence

@dataclass(order=True)
class pnode(node):
    def __init__(self, coordinates = (0,0), path = (), tax: float = 0, action_sequence = ()):
        super().__init__(coordinates, path, tax, action_sequence)
        self.priority = tax
        self.item: Any = field(compare=False)
    priority: float
    # item: Any

def ExpandNode(current: pnode):
    global queue
    if not current.available_dir:
        return
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
        toNode = pnode(coordinates=to_coordinates, path=path, tax=tax, action_sequence=action_sequence)
        heapq.heappush(queue, toNode)
    return

def GoalTest(node: node):
    return node.coordinates == (m-1,n-1)


def Solution(node: node):
    # global best_tax, best_action_sequence
    # if node.tax < best_tax:
    #     best_tax = node.tax
    #     best_action_sequence = node.action_sequence
    print("The optimal action sequence is:", node.action_sequence)
    print("which corresponds to the minimal tax:", node.tax)
    return

def PilgrimBredthFirst():
    global queue
    while queue:
        current = heapq.heappop(queue)
        if GoalTest(current):
            Solution(current)
            del current
            return
        else:
            ExpandNode(current)
            del current
    print(best_tax)
    print(best_action_sequence)
    return

if __name__ == '__main__':
    # m = int(input('m = '))
    # n = int(input('n = '))
    # initial_sequence = input('Starting action_sequence (West: w, East: e, North: n, South: s): ').split()
    # random.seed(7)
    with open('data/data4.txt', 'r') as data:
        m = int(data.readline())
        n = int(data.readline())
        initial_sequence = data.readline().split()
        random.seed(data.readline())
    cost = {}
    cost['w'] = random.randint(2, 5)
    cost['e'] = random.randint(2, 5)
    cost['s'] = random.randint(2, 5)
    cost['n'] = random.randint(2, 5)
    print('m = ', m)
    print('n = ', n)
    print('Initial sequence is: ', initial_sequence)
    print("Going East will increase the tax by", cost['e'])
    print('Going West will decrease the tax by', cost['w'])
    print('Going South will multiply the tax by', cost['s'])
    print('Going North will divide the tax by', cost['n'])
    heuristics = np.zeros((m+1,n+1))
    for i in range(m+1):
        for j in range(n+1):
            heuristics[i,j] = math.exp((((cost['e'] * (m-i)) / (cost['n'] ** (j+1)) - (cost['w'] * n)) * (cost['s'] ** (m+1)) + (cost['e'] * n)))
            # heuristics[i, j] = math.exp((cost['e'] * (n-j)) * (cost['s'] ** (m-i)))
    heuristics[m,n] = 0
    queue = []
    initial_tax = 0
    point = (0, 0)
    # next = ()
    initial_path = []
    for dir in initial_sequence:
        if dir == 'w':
            initial_tax -= cost[dir]
            next = (point[0], point[1] - 1)
            initial_path.append({point, next})
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
    heapq.heappush(queue, pnode(coordinates=point, tax=initial_tax, path=tuple(initial_path), action_sequence= tuple(initial_sequence)))
    best_tax = 10e9
    best_action_sequence = ()
    t0 = timeit.default_timer()
    PilgrimBredthFirst()
    print("Time taken to solve this problem:", timeit.default_timer() - t0)
    best_path = [(0, 0)]
    for movement in best_action_sequence:
        if movement == 'w':
            best_path.append((best_path[-1][0], best_path[-1][1] - 1))
        elif movement == 'e':
            best_path.append((best_path[-1][0], best_path[-1][1] + 1))
        elif movement == 'n':
            best_path.append((best_path[-1][0] - 1, best_path[-1][1]))
        elif movement == 's':
            best_path.append((best_path[-1][0] + 1, best_path[-1][1]))
