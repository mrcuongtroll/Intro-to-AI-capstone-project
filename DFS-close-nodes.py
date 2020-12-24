from time import perf_counter
m = 5
n = 5

# move_cost: up, down, left, right
move_cost = [2, 2, 2, 2]


class Point:
    def __init__(self, coordinate, current_cost):
        self.coordinate = coordinate
        # possible_move: up, down, left, right
        self.possible_move = [1, 1, 1, 1]

    def go_up(self):
        new_position = list(self.coordinate)
        if new_position[0] < 0:
            return None
        else:
            new_position[0] -= 1
            return tuple(new_position)

    def go_down(self):
        new_position = list(self.coordinate)
        if new_position[0] > n - 1:
            return None
        else:
            new_position[0] += 1
            return tuple(new_position)

    def go_left(self):
        new_position = list(self.coordinate)
        if new_position[1] < 0:
            return None
        else:
            new_position[1] -= 1
            return tuple(new_position)

    def go_right(self):
        new_position = list(self.coordinate)
        if new_position[1] > n - 1:
            return None
        else:
            new_position[1] += 1
            return tuple(new_position)

    def get_position(self):
        return self.coordinate


closed_nodes = []
all_points = {}
for i in range(m):
    for j in range(n):
        all_points[(i, j)] = Point((i, j), 0)
for i in range(1,m):
    all_points[(i, 0)].possible_move = [1, 1, 0, 1]
    all_points[(i, n-1)].possible_move = [1, 1, 1, 0]
for j in range(1,n):
    all_points[(0, j)].possible_move = [0, 1, 1, 1]
    all_points[(m-1, j)].possible_move = [1, 0, 1, 1]
all_points[(0, 0)].possible_move = [0, 1, 0, 1]
all_points[(m-1, 0)].possible_move = [1, 0, 0, 1]
all_points[(0, n-1)].possible_move = [0, 1, 1, 0]
all_points[(m - 1, n - 1)].possible_move = [0, 0, 0, 0]

stack_path = [[all_points[(0, 0)]]]
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


def restrict(current_node, dir):  # Cant go through the same path, return next node coordinate
    if dir == 0:  # Up
        new_coordinate = current_node.go_up()
        all_points[new_coordinate].possible_move[1] = 0
        current_node.possible_move[0] = 0
    if dir == 1:  # Down
        new_coordinate = current_node.go_down()
        all_points[new_coordinate].possible_move[0] = 0
        current_node.possible_move[1] = 0
    if dir == 2:  # Left
        new_coordinate = current_node.go_left()
        all_points[new_coordinate].possible_move[3] = 0
        current_node.possible_move[2] = 0
    if dir == 3:  # Right
        new_coordinate = current_node.go_right()
        all_points[new_coordinate].possible_move[2] = 0
        current_node.possible_move[3] = 0
    return new_coordinate


def unrestrict(current_node, dir):  # undo restrict
    if dir == 0:  # Up
        if current_node.go_up() is not None:
            new_coordinate = current_node.go_up()
            all_points[new_coordinate].possible_move[1] = 1
            current_node.possible_move[0] = 1
    if dir == 1:  # Down
        if current_node.go_down() is not None:
            new_coordinate = current_node.go_down()
            all_points[new_coordinate].possible_move[0] = 1
            current_node.possible_move[1] = 1
    if dir == 2:  # Left
        if current_node.go_left() is not None:
            new_coordinate = current_node.go_left()
            all_points[new_coordinate].possible_move[3] = 1
            current_node.possible_move[2] = 1
    if dir == 3:  # Right
        if current_node.go_right() is not None:
            new_coordinate = current_node.go_right()
            all_points[new_coordinate].possible_move[2] = 1
            current_node.possible_move[3] = 1


def close_node(current_considered_node, new_coordinate):
    if current_considered_node == all_points[new_coordinate]:
        return
    if current_considered_node.possible_move.count(1)==1:
        dir_to_remove = current_considered_node.possible_move.index(1)
        new_node_coor = restrict(current_considered_node, dir_to_remove)
        closed_nodes[-1].append((current_considered_node, dir_to_remove))
        close_node(all_points[new_node_coor], new_coordinate)


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
                    current_path.append(all_points[new_coordinate])
                    closed_nodes.append([])
                    stack_cost[-1] /= move_cost[0]
                    restrict(current_node, 0)
                    close_node(current_node, new_coordinate)
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path)
                    elif current_path[-1].possible_move != [0, 0, 0, 0]:
                        stack_path.append(current_path)
                        DFS()
                    current_path.pop()
                    to_unclose_node = closed_nodes[-1][:]
                    for (node, dir) in to_unclose_node:
                        unrestrict(node, dir)
                    closed_nodes.pop()
                    unrestrict(current_node, 0)
            elif v == 1:
                if current_node.go_down() is not None:
                    new_coordinate = current_node.go_down()
                    current_path.append(all_points[new_coordinate])
                    closed_nodes.append([])
                    stack_cost[-1] *= move_cost[1]
                    restrict(current_node, 1)
                    close_node(current_node, new_coordinate)
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path)
                    elif current_path[-1].possible_move != [0, 0, 0, 0]:
                        stack_path.append(current_path)
                        DFS()
                    current_path.pop()
                    to_unclose_node = closed_nodes[-1][:]
                    for (node, dir) in to_unclose_node:
                        unrestrict(node, dir)
                    closed_nodes.pop()
                    unrestrict(current_node, 1)
            elif v == 2:
                if current_node.go_left() is not None:
                    new_coordinate = current_node.go_left()
                    current_path.append(all_points[new_coordinate])
                    closed_nodes.append([])
                    stack_cost[-1] -= move_cost[2]
                    restrict(current_node, 2)
                    close_node(current_node, new_coordinate)
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path)
                    elif current_path[-1].possible_move != [0, 0, 0, 0]:
                        stack_path.append(current_path)
                        DFS()
                    current_path.pop()
                    to_unclose_node = closed_nodes[-1][:]
                    for (node, dir) in to_unclose_node:
                        unrestrict(node, dir)
                    closed_nodes.pop()
                    unrestrict(current_node, 2)
            elif v == 3:
                if current_node.go_right() is not None:
                    new_coordinate = current_node.go_right()
                    current_path.append(all_points[new_coordinate])
                    closed_nodes.append([])
                    stack_cost[-1] += move_cost[3]
                    restrict(current_node, 3)
                    close_node(current_node, new_coordinate)
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path)
                    elif current_path[-1].possible_move != [0, 0, 0, 0]:
                        stack_path.append(current_path)
                        DFS()
                    current_path.pop()
                    to_unclose_node = closed_nodes[-1][:]
                    for (node, dir) in to_unclose_node:
                        unrestrict(node, dir)
                    closed_nodes.pop()
                    unrestrict(current_node, 3)
