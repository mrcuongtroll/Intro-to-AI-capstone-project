import math
import random

random.seed(101)

m = int(input('M: '))
n = int(input('N: '))

initial_sequence = input('Starting action_sequence (West: w, East: e, North: n, South: s): ').split()

# move_cost: North, South, West, East
# move_cost = [2, 2, 2, 2]
move_cost = [random.randint(2, 5), random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)]


class Point:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        # possible_move: North, South, West, East
        self.possible_move = [1, 1, 1, 1]

    def go_up(self):
        new_position = list(self.coordinate)
        if new_position[0] <= 0:
            return None
        else:
            new_position[0] -= 1
            return tuple(new_position)

    def go_down(self):
        new_position = list(self.coordinate)
        if new_position[0] >= m - 1:
            return None
        else:
            new_position[0] += 1
            return tuple(new_position)

    def go_left(self):
        new_position = list(self.coordinate)
        if new_position[1] <= 0:
            return None
        else:
            new_position[1] -= 1
            return tuple(new_position)

    def go_right(self):
        new_position = list(self.coordinate)
        if new_position[1] >= n - 1:
            return None
        else:
            new_position[1] += 1
            return tuple(new_position)

    def get_position(self):
        return self.coordinate


all_points = []
for i in range(m):
    row = []
    for j in range(n):
        row.append(Point((i, j)))
    all_points.append(row)

all_points[0][0].possible_move = [0, 1, 0, 1]
all_points[m - 1][n - 1].possible_move = [0, 0, 0, 0]
initial_path = [all_points[0][0]]
stack_cost = [0]
min_cost = 999
count = 0
best_path = []

for s in initial_sequence:
    if s == 'n':
        new_coordinate = initial_path[-1].go_up()
        if new_coordinate is not None:
            initial_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
            initial_path[-2].possible_move[0] = 0
            initial_path[-1].possible_move[1] = 0
            stack_cost[0] /= move_cost[0]
    elif s == 's':
        new_coordinate = initial_path[-1].go_down()
        if new_coordinate is not None:
            initial_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
            initial_path[-2].possible_move[1] = 0
            initial_path[-1].possible_move[0] = 0
            stack_cost[0] *= move_cost[1]
    elif s == 'w':
        new_coordinate = initial_path[-1].go_left()
        if new_coordinate is not None:
            initial_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
            initial_path[-2].possible_move[2] = 0
            initial_path[-1].possible_move[3] = 0
            stack_cost[0] -= move_cost[2]
    elif s == 'e':
        new_coordinate = initial_path[-1].go_right()
        if new_coordinate is not None:
            initial_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
            initial_path[-2].possible_move[3] = 0
            initial_path[-1].possible_move[2] = 0
            stack_cost[0] += move_cost[3]
stack_path = [initial_path]


def Solution(current_path, current_cost):
    global min_cost, all_points, best_path, count
    if current_cost < min_cost:
        min_cost = current_cost
        count += 1
        print('Count: ', count)
        print('Current minimum cost:', current_cost)
        print('Current optimal path:')
        best_path = [x.get_position() for x in current_path]
        print(best_path)
        print('\n')


def BoundingObsolete(current_cost, current_path):
    global all_points, min_cost, best_path
    if (current_cost + 1000 - max(move_cost[2], move_cost[3]) * (n - current_path[-1].get_position()[1])) / (
            max(move_cost[0], move_cost[1]) ** (m - current_path[-1].get_position()[1])) < min_cost + 1000:
        return True
    else:
        return False


def Bounding(current_cost, current_path):
    global all_points, min_cost, best_path
    if math.exp(current_cost / 10000) / (
            max(move_cost[0], move_cost[1]) ** (
            (m - current_path[-1].get_position()[0]) * (n - current_path[-1].get_position()[1]))) < math.exp(
            min_cost / 10000):
        return True
    else:
        return False


def DFS():
    global stack_path, min_cost, move_cost, all_points, stack_cost, count, best_path
    if len(stack_path) == 0:
        return
    current_path = stack_path.pop()
    current_cost = stack_cost.pop()
    current_node = current_path[-1]
    for v in range(4):
        if current_node.possible_move[v] == 1:
            if v == 0:
                if current_node.go_up() is not None:
                    new_coordinate = current_node.go_up()
                    current_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
                    current_cost /= move_cost[0]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[1] = 0
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[0] = 0
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path, current_cost)
                    elif current_path[-1].possible_move != [0, 0, 0, 0] and Bounding(current_cost,
                                                                                     current_path):
                        stack_path.append(current_path)
                        stack_cost.append(current_cost)
                        DFS()
                    current_path.pop()
                    current_cost *= move_cost[0]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[1] = 1
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[0] = 1
            elif v == 1:
                if current_node.go_down() is not None:
                    new_coordinate = current_node.go_down()
                    current_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
                    current_cost *= move_cost[1]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[0] = 0
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[1] = 0
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path, current_cost)
                    elif current_path[-1].possible_move != [0, 0, 0, 0] and Bounding(current_cost,
                                                                                     current_path):
                        stack_path.append(current_path)
                        stack_cost.append(current_cost)
                        DFS()
                    current_path.pop()
                    current_cost /= move_cost[1]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[0] = 1
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[1] = 1
            elif v == 2:
                if current_node.go_left() is not None:
                    new_coordinate = current_node.go_left()
                    current_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
                    current_cost -= move_cost[2]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[3] = 0
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[2] = 0
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path, current_cost)
                    elif current_path[-1].possible_move != [0, 0, 0, 0] and Bounding(current_cost,
                                                                                     current_path):
                        stack_path.append(current_path)
                        stack_cost.append(current_cost)
                        DFS()
                    current_path.pop()
                    current_cost += move_cost[2]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[3] = 1
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[2] = 1
            elif v == 3:
                if current_node.go_right() is not None:
                    new_coordinate = current_node.go_right()
                    current_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
                    current_cost += move_cost[3]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[2] = 0
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[3] = 0
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path, current_cost)
                    elif current_path[-1].possible_move != [0, 0, 0, 0] and Bounding(current_cost,
                                                                                     current_path):
                        stack_path.append(current_path)
                        stack_cost.append(current_cost)
                        DFS()
                    current_path.pop()
                    current_cost -= move_cost[3]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[2] = 1
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[3] = 1


DFS()
