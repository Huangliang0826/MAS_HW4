import random

# A single unit of the Grid.
class Cell:
  def __init__(self, x_position,y_position, type, reward):
    self.x_position = x_position
    self.y_position = y_position
    self.type = type
    self.reward = reward
    self.east = random.uniform(-1,1)
    self.west = random.uniform(-1,1)
    self.south = random.uniform(-1,1)
    self.north = random.uniform(-1,1)

# Grid matrix, globale variable
grid = []
map_length = 0
map_height = 0
epsilon = 0.1
learning_rate = 0.5
discounting_factor = 0.9

# Map of given parameters.
class Map:
    def __init__(self, length, height, wall_positions, treasure_positions, terminate_states):
        self.length = length
        self.height = height
        self.wall_positions = wall_positions
        self.treasure_positions = treasure_positions
        self.terminate_states = terminate_states
        map_length = length
        map_height = height

        for row in range(height):
            grid.append([])
            for column in range(length):
                current_location = (row, column)
                # check if this position is wall.
                if current_location in wall_positions:
                    cell = Cell(row, column, "wall", -1)
                # check if this position is treasure.
                elif current_location in treasure_positions:
                    cell = Cell(row, column, "treasure", 10)
                # check if this position is terminate state.
                elif current_location in terminate_states:
                    cell = Cell(row, column, "terminate", -20)
                else:
                    cell = Cell(row, column, "state",-1)

                grid[row].append(cell)

def e_greedy_action(state_x, state_y):
    if random.uniform(0,1) > epsilon:
        state_action_value = [];
        state_action_value.append(grid[state_x][state_y].east)
        state_action_value.append(grid[state_x][state_y].west)
        state_action_value.append(grid[state_x][state_y].south)
        state_action_value.append(grid[state_x][state_y].north)
        # print("Greedy Action:")
        # print(state_action_value)
        selected_action = state_action_value.index(max(state_action_value))
    else:
        # print("Random Action:")
        selected_action = random.randint(0,3)

    if selected_action == 0:
        return "east"
    elif selected_action == 1:
        return "west"
    elif selected_action == 2:
        return "south"
    elif selected_action == 3:
        return "north"
    else:
        return "error"

def random_action():
    # print("Random Action:")
    selected_action = random.randint(0, 3)

    if selected_action == 0:
        return "east"
    elif selected_action == 1:
        return "west"
    elif selected_action == 2:
        return "south"
    elif selected_action == 3:
        return "north"
    else:
        return "error"

# According to the give action, this function can calculate the position adjustment to be performed.
def calculate_adjustment(action_taken):
    adjustment = []
    if action_taken == "east":
        adjustment = [1,0]
    elif action_taken == "west":
        adjustment = [-1,0]
    elif action_taken == "south":
        adjustment = [0,1]
    elif action_taken == "north":
        adjustment = [0,-1]
    else:
        adjustment = [0,0]
    return adjustment

def check_out_of_bound(given_index_x, given_index_y):
    if given_index_x >7 or given_index_x < 0 or given_index_y >7 or given_index_y < 0:
        return True
    elif grid[given_index_x][given_index_y].type == "wall":
        return True
    else:
        return False



# Test cell class
cell_1 = Cell(1,2,'wall',-1)

print('x_position : %s'%cell_1.x_position)
print('y_position : %s'%cell_1.y_position)
print('Cell type: %s'%cell_1.type)


# Initialise the Map Grid
wall_positions = [(2,1),(3,1),(4,1),(5,1),(5,1),(5,2),(5,3),(5,4),(1,6),(2,6),(3,6)]
treasure_positions = [(7,7)]
terminate_states = [(4,5)]

map = Map(8,8, wall_positions,treasure_positions,terminate_states)


print(grid[4][5].type)

# Print the map for checking
for row in range(map_height):
    for column in range(map_length):
        print(grid[column][row].type),
    print('')

# SARSA ALgorithm
# Build a q-value look up dictionary.
# Random initialise the q-value table.
# E.g. print(grid[2][1].east)
# print(grid[1][1].east)
# print(grid[1][1].west)
# print(grid[1][1].south)
# print(grid[1][1].north)

# For each episode
for episode in range(10000):

    print('Episode %i'%episode)

    # Initialise the start state.
    start_x = random.randint(0,7)
    start_y = random.randint(0,7)

    # if episode == 99:
    print('X Position: {} . Y Position: {}.'.format(start_x,start_y))
    # print(start_x,start_y)
    next_x = start_x
    next_y = start_y

    if grid[next_x][next_x].type == "wall":
        continue
    elif grid[next_x][next_x].type == "treasure":
        continue

    # Choose an action a from given policy, here is the e-greedy policy
    action = e_greedy_action(start_x,start_y)
    # print(action)

    step = 0
    # For each episode step
    while grid[next_x][next_y].type != "terminate" and grid[next_x][next_y].type !="treasure":
        # print("Step {}: {}. (x,y)=({},{})".format(step, action, next_x, next_y))
        step+=1
        adjust = calculate_adjustment(action)
        outofbound = check_out_of_bound(next_x+adjust[0],next_y+adjust[1])
        if outofbound:
            # Perform the action and observe the r and s'
            action_reward = -1
            current_state = grid[next_x][next_y]
            next_state = grid[next_x][next_y]
            # Choose a' from s' using policy derive from Q
            next_action = random_action()

            next_state_action_value = -1

            # Q(s,a) += alpha * (r + gamma * Q(s', a') - Q(s,a))
            if action == 'east':
                current_state.east += learning_rate * (
                    action_reward + discounting_factor * next_state_action_value - current_state.east)
            elif action == 'west':
                current_state.west += learning_rate * (
                    action_reward + discounting_factor * next_state_action_value - current_state.west)
            elif action == 'south':
                current_state.south += learning_rate * (
                    action_reward + discounting_factor * next_state_action_value - current_state.south)
            else:
                current_state.north += learning_rate * (
                action_reward + discounting_factor * next_state_action_value - current_state.north)

            # state = next_state, action = next_action
            action = next_action

            #Need to change actions.
        else:
            # Perform the action and observe the r and s'
            action_reward = 0
            if grid[next_x+adjust[0]][next_y+adjust[1]].type == 'treasure':
                action_reward = 10
            elif grid[next_x+adjust[0]][next_y+adjust[1]].type == 'terminate':
                action_reward = -20
            else:
                action_reward = -1
            current_state = grid[next_x][next_y]
            next_x += adjust[0]
            next_y += adjust[1]
            next_state = grid[next_x][next_y]

            # Choose a' from s' using policy derive from Q
            next_action = e_greedy_action(next_x,next_y)

            if next_action == 'east':
                next_state_action_value = next_state.east
            elif next_action == 'west':
                next_state_action_value = next_state.west
            elif next_action == 'south':
                next_state_action_value = next_state.south
            else:
                next_state_action_value = next_state.north

            # Q(s,a) += alpha * (r + gamma * Q(s', a') - Q(s,a))
            if action == 'east':
                current_state.east += learning_rate * (
                action_reward + discounting_factor * next_state_action_value - current_state.east)
            elif action == 'west':
                current_state.west += learning_rate * (
                action_reward + discounting_factor * next_state_action_value - current_state.west)
            elif action == 'south':
                current_state.south += learning_rate * (
                action_reward + discounting_factor * next_state_action_value - current_state.south)
            else:
                current_state.north += learning_rate*(action_reward + discounting_factor*next_state_action_value - current_state.north)

            # state = next_state, action = next_action
            action = next_action
    print("Step {}: {}. (x,y)=({},{})".format(step, action, next_x, next_y))





