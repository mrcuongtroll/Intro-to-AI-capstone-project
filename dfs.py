m = 6
n = 6

# move_cost: up, down, left, right
move_cost = [2, 2, 2, 2]


class Point:
    def __init__(self, coordinate, current_cost):
        self.coordinate = coordinate
        # possible_move: up, down, left, right
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
        if new_position[0] >= n - 1:
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
        row.append(Point((i, j), 0))
    all_points.append(row)

all_points[0][0].possible_move = [0, 1, 0, 1]
all_points[m - 1][n - 1].possible_move = [0, 0, 0, 0]
stack_path = [[all_points[0][0]]]
stack_cost = [0]
min_cost = 9999999


def Solution(current_path):
    global min_cost, all_points
    cost = 0
    for i in range(1, len(current_path)):
        if current_path[i].get_position()[0] == current_path[i - 1].get_position()[0]:
            if current_path[i].get_position()[1] - current_path[i - 1].get_position()[1] == 1:
                cost += 2
            else:
                cost -= 2
        else:
            if current_path[i].get_position()[0] - current_path[i - 1].get_position()[0] == 1:
                cost *= 2
            else:
                cost /= 2
    if cost < min_cost:
        min_cost = cost
        print('Current minimum cost:', cost)
        print('Current optimal path:')
        print([x.get_position() for x in current_path])
        print('\n\n')


def DFS():
    global stack_path, min_cost, move_cost, all_points, stack_cost, count
    if len(stack_path) == 0:
        return
    current_path = stack_path.pop()
    current_node = current_path[-1]
    for v in range(4):
        if current_node.possible_move[v] == 1:
            if v == 0:
                if current_node.go_up() is not None:
                    new_coordinate = current_node.go_up()
                    current_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
                    stack_cost[-1] /= move_cost[0]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[1] = 0
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[0] = 0
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path)
                    elif current_path[-1].possible_move != [0, 0, 0, 0]:
                        stack_path.append(current_path)
                        DFS()
                    current_path.pop()
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[1] = 1
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[0] = 1
            elif v == 1:
                if current_node.go_down() is not None:
                    new_coordinate = current_node.go_down()
                    current_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
                    stack_cost[-1] *= move_cost[1]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[0] = 0
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[1] = 0
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path)
                    elif current_path[-1].possible_move != [0, 0, 0, 0]:
                        stack_path.append(current_path)
                        DFS()
                    current_path.pop()
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[0] = 1
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[1] = 1
            elif v == 2:
                if current_node.go_left() is not None:
                    new_coordinate = current_node.go_left()
                    current_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
                    stack_cost[-1] -= move_cost[2]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[3] = 0
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[2] = 0
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path)
                    elif current_path[-1].possible_move != [0, 0, 0, 0]:
                        stack_path.append(current_path)
                        DFS()
                    current_path.pop()
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[3] = 1
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[2] = 1
            elif v == 3:
                if current_node.go_right() is not None:
                    new_coordinate = current_node.go_right()
                    current_path.append(all_points[new_coordinate[0]][new_coordinate[1]])
                    stack_cost[-1] += move_cost[3]
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[2] = 0
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[3] = 0
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path)
                    elif current_path[-1].possible_move != [0, 0, 0, 0]:
                        stack_path.append(current_path)
                        DFS()
                    current_path.pop()
                    all_points[new_coordinate[0]][new_coordinate[1]].possible_move[2] = 1
                    all_points[current_node.get_position()[0]][current_node.get_position()[1]].possible_move[3] = 1


DFS()
