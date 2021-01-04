import random
random.seed(101)
m = int(input('M: '))
n = int(input('N: '))

initial_sequence = input('Starting action_sequence (West: w, East: e, North: n, South: s): ').split()

# move_cost: North, South, West, East
move_cost = [random.randint(2, 5), random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)]

class Point:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        # possible_move: North, South, West, East
        self.possible_move = [1, 1, 1, 1]

    def go_up(self):
        new_position = list(self.coordinate)
        if new_position[0] < 0:
            return False
        else:
            new_position[0] -= 1
            return tuple(new_position)

    def go_down(self):
        new_position = list(self.coordinate)
        if new_position[0] > m - 1:
            return False
        else:
            new_position[0] += 1
            return tuple(new_position)

    def go_left(self):
        new_position = list(self.coordinate)
        if new_position[1] < 0:
            return False
        else:
            new_position[1] -= 1
            return tuple(new_position)

    def go_right(self):
        new_position = list(self.coordinate)
        if new_position[1] > n - 1:
            return False
        else:
            new_position[1] += 1
            return tuple(new_position)

    def get_position(self):
        return self.coordinate
 
cost_dict = {}
closed_nodes = []
all_points = {}
best_cost={}
for i in range(m):
    for j in range(n):
        all_points[(i, j)] = Point((i, j))
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
initial_path = [all_points[(0,0)]]
initial_cost = [0]

min_cost = 999999
count = 0
best_path = []
initial_path = [all_points[(0,0)]]
stack_cost = [0]


for s in initial_sequence:
    if s == 'n':
        new_coordinate = initial_path[-1].go_up()
        if new_coordinate is not False:
            initial_path.append(all_points[new_coordinate])
            initial_path[-2].possible_move[0] = 0
            initial_path[-1].possible_move[1] = 0
            stack_cost[0] /= move_cost[0]
    elif s == 's':
        new_coordinate = initial_path[-1].go_down()
        if new_coordinate is not False:
            initial_path.append(all_points[new_coordinate])
            initial_path[-2].possible_move[1] = 0
            initial_path[-1].possible_move[0] = 0
            stack_cost[0] *= move_cost[1]
    elif s == 'w':
        new_coordinate = initial_path[-1].go_left()
        if new_coordinate is not False:
            initial_path.append(all_points[new_coordinate])
            initial_path[-2].possible_move[2] = 0
            initial_path[-1].possible_move[3] = 0
            stack_cost[0] -= move_cost[2]
    elif s == 'e':
        new_coordinate = initial_path[-1].go_right()
        if new_coordinate is not False:
            initial_path.append(all_points[new_coordinate])
            initial_path[-2].possible_move[3] = 0
            initial_path[-1].possible_move[2] = 0
            stack_cost[0] += move_cost[3]
def_cost = stack_cost[:]

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
    
def close_node_initial(current_considered_node):
    if current_considered_node == all_points[(m - 1, n - 1)] or current_considered_node == initial_path[-1]:
        return
    if current_considered_node.possible_move.count(1)==1:
        dir_to_remove = current_considered_node.possible_move.index(1)
        new_node_coor = restrict(current_considered_node, dir_to_remove)
        close_node_initial(all_points[new_node_coor])
        
for node in initial_path:
    close_node_initial(node)
    
stack_path = [initial_path]

def Solution(current_path, current_cost):
    global min_cost, all_points, best_path, count, best_cost
    path=(x.get_position() for x in current_path[:])
    if len(current_path) not in best_cost:
        best_cost[len(current_path)]=current_cost
    else:
        if best_cost[len(current_path)]>current_cost:
            best_cost[len(current_path)]=current_cost
    if current_cost < min_cost:
        min_cost = current_cost
        count += 1
        print('Count: ', count)
        print('Current minimum cost:', current_cost)
        print('Current optimal path:')
        best_path = [x.get_position() for x in current_path]
        print(best_path)
        print('Length of optimal path:', len(best_path))
        print('\n')
        
def loop_check(new_node,current_path,stack_cost):
    if new_node in current_path[:-1]:
        key = tuple(current_path)
        if key in cost_dict:
          if stack_cost >= cost_dict[key]:
              del(cost_dict[key])
              return False
          else:
            del(cost_dict[key])
            return True
        else:
          i = current_path.index(new_node,0,-1)
          corresponding_path = tuple(current_path[0:i].copy()+current_path[-1:i-1:-1].copy())
          cost_dict[corresponding_path] = stack_cost
          return True
    else: 
      return True

def unrestrict(current_node, dir):  # undo restrict
    if current_node != all_points[(m - 1, n - 1)]:
        if dir == 0:  # Up
            if current_node.go_up() is not False:
                new_coordinate = current_node.go_up()
                all_points[new_coordinate].possible_move[1] = 1
                current_node.possible_move[0] = 1
        if dir == 1:  # Down
            if current_node.go_down() is not False:
                new_coordinate = current_node.go_down()
                all_points[new_coordinate].possible_move[0] = 1
                current_node.possible_move[1] = 1
        if dir == 2:  # Left
            if current_node.go_left() is not False:
                new_coordinate = current_node.go_left()
                all_points[new_coordinate].possible_move[3] = 1
                current_node.possible_move[2] = 1
        if dir == 3:  # Right
            if current_node.go_right() is not False:
                new_coordinate = current_node.go_right()
                all_points[new_coordinate].possible_move[2] = 1
                current_node.possible_move[3] = 1

 
def close_node(current_considered_node,new_coordinate):
    if current_considered_node == all_points[(m - 1, n - 1)] or current_considered_node ==all_points[(new_coordinate)]:
        return
    if current_considered_node.possible_move.count(1)==1:
        dir_to_remove = current_considered_node.possible_move.index(1)
        new_node_coor = restrict(current_considered_node, dir_to_remove)
        closed_nodes[-1].append((current_considered_node, dir_to_remove))
        close_node(all_points[new_node_coor],new_coordinate)
        
def manhattan_calc(current_node): #calculate the min. number of path to reach the goal
    i,j =current_node.coordinate
    return m-1-i+n-1-j
    
def BacktrackingIterStart(depth):
    global stack_path, min_cost, move_cost, all_points, stack_cost, count, best_path
    stack_path = [initial_path[:]]
    stack_cost = def_cost[:]
    BacktrackingIter(depth)

def BacktrackingIter(depth):
    global stack_path, min_cost, move_cost, all_points, stack_cost, count, best_path
    if len(stack_path) == 0:
        return
      
    current_path = stack_path.pop()
    current_cost = stack_cost.pop()
    current_node = current_path[-1]
    if manhattan_calc(current_node) > depth - len(current_path):
        return
    for v in range(4):
        if current_node.possible_move[v] == 1:
            if v == 0:
                if current_node.go_up() is not False:
                    new_coordinate = current_node.go_up()
                    new_node = all_points[new_coordinate]
                    current_path.append(all_points[new_coordinate])
                    closed_nodes.append([])
                    current_cost /= move_cost[0]
                    restrict(current_node, 0)
                    close_node(current_node,new_coordinate)
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path, current_cost)
                    elif current_path[-1].possible_move != [0, 0, 0, 0] and loop_check(new_node,current_path,current_cost):
                        stack_path.append(current_path)
                        stack_cost.append(current_cost)
                        BacktrackingIter(depth)
                    current_path.pop()
                    current_cost *= move_cost[0]
                    to_unclose_node = closed_nodes.pop()
                    for (node, dir) in to_unclose_node:
                        unrestrict(node, dir)
                    unrestrict(current_node, 0)
            elif v == 1:
                if current_node.go_down() is not False:
                    new_coordinate = current_node.go_down()
                    new_node = all_points[new_coordinate]
                    current_path.append(all_points[new_coordinate])
                    closed_nodes.append([])
                    current_cost *= move_cost[1]
                    restrict(current_node, 1)
                    close_node(current_node,new_coordinate)
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path, current_cost)
                    elif current_path[-1].possible_move != [0, 0, 0, 0] and loop_check(new_node,current_path,current_cost):
                        stack_path.append(current_path)
                        stack_cost.append(current_cost)
                        BacktrackingIter(depth)
                    current_path.pop()
                    current_cost /= move_cost[1]
                    to_unclose_node = closed_nodes.pop()
                    for (node, dir) in to_unclose_node:
                        unrestrict(node, dir)
                    unrestrict(current_node, 1)
            elif v == 2:
                if current_node.go_left() is not False:
                    new_coordinate = current_node.go_left()
                    new_node = all_points[new_coordinate]
                    current_path.append(all_points[new_coordinate])
                    closed_nodes.append([])
                    current_cost -= move_cost[2]
                    restrict(current_node, 2)
                    close_node(current_node,new_coordinate)
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path, current_cost)
                    elif current_path[-1].possible_move != [0, 0, 0, 0] and loop_check(new_node,current_path,current_cost):
                        stack_path.append(current_path)
                        stack_cost.append(current_cost)
                        BacktrackingIter(depth)
                    current_path.pop()
                    current_cost += move_cost[2]
                    to_unclose_node = closed_nodes.pop()
                    for (node, dir) in to_unclose_node:
                        unrestrict(node, dir)
                    unrestrict(current_node, 2)
            elif v == 3:
                if current_node.go_right() is not False:
                    new_coordinate = current_node.go_right()
                    new_node = all_points[new_coordinate]
                    current_path.append(all_points[new_coordinate])
                    closed_nodes.append([])
                    current_cost += move_cost[3]
                    restrict(current_node, 3)
                    close_node(current_node,new_coordinate)
                    if current_path[-1].get_position() == (m - 1, n - 1):
                        Solution(current_path, current_cost)
                    elif current_path[-1].possible_move != [0, 0, 0, 0] and loop_check(new_node,current_path,current_cost):
                        stack_path.append(current_path)
                        stack_cost.append(current_cost)
                        BacktrackingIter(depth)
                    current_path.pop()
                    current_cost -= move_cost[3]
                    to_unclose_node = closed_nodes.pop()
                    for (node, dir) in to_unclose_node:
                        unrestrict(node, dir)
                    unrestrict(current_node, 3)

i = manhattan_calc(initial_path[0])+1
iter_count = 0
while True:
    old_best_cost = len(best_cost)
    BacktrackingIterStart(i)
    updated = old_best_cost != len(best_cost)
    if len(best_cost)>=1 and not updated: #preventing unlimited run
        if iter_count >= 4:
            break
        else: iter_count += 1
    if len(best_cost)>=4:
        if len(best_cost) !=0 and not updated :
            break
        if min_cost <= 0 and best_cost[i]>best_cost[i-2] and best_cost[i]>best_cost[i-4]:
            break
    i+=2
