"""Find optimal policy in a grid world using SARSA algorithm.

Author: Liang Huang
Date: 04/Nov/2018
Email: huangliang0826@icloud.com

This script allows the user to calculate the optimal policy given a
grid world map.

This file can also be imported as a module and contains the following
functions:
    * Cell: The most basic building block of the map.
    * Map: All the information we need to construct a virtual environment
        for agents to explore.

This file can also be imported as a module and contains the following
functions:
    * e_greedy_action(state_x, state_y): Epsilon-greedy action from state_x to state_y.
    * random_action(): return "west" or "east" or "south" or "north" randomly.
    * calculate_adjustment(action_taken): Calculate the position adjustment to be performed,
                                        According to the give action.
    * check_out_of_bound(given_index_x, given_index_y): Check whether the given position is a
                                    wall or out of bound on the map.
    * SARSA_algorithm: To find the best policy by using on-policy TD strategy.

This script requires that `ramdom` be imported within the Python
environment you are running this script in.

"""
import random

random.seed(0)

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

# Grid matrix, global variable
grid = []
map_length = 8
map_height = 8
epsilon = 0
learning_rate = 0.1
discounting_factor = 0.99

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
        state_action_value = []
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

def greedy_action(state_x, state_y):
    if grid[state_x][state_y].type == "wall":
        return 'W'
    elif grid[state_x][state_y].type == "terminate":
        return 'S'
    elif grid[state_x][state_y].type == "treasure":
        return 'T'
    state_action_value = []
    state_action_value.append(grid[state_x][state_y].east)
    state_action_value.append(grid[state_x][state_y].west)
    state_action_value.append(grid[state_x][state_y].south)
    state_action_value.append(grid[state_x][state_y].north)
    # print("Greedy Action:")
    # print(state_action_value)
    selected_action = state_action_value.index(max(state_action_value))
    if selected_action == 0:
        return "\u2192"
    elif selected_action == 1:
        return "\u2190"
    elif selected_action == 2:
        return "\u2193"
    elif selected_action == 3:
        return "\u2191"
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
def test_cells():
    cell_1 = Cell(1,2,'wall',-1)

    print('x_position : %s'%cell_1.x_position)
    print('y_position : %s'%cell_1.y_position)
    print('Cell type: %s'%cell_1.type)

# Initialise the Map Grid
wall_positions = [(2,1),(3,1),(4,1),(5,1),(5,1),(5,2),(5,3),(5,4),(1,6),(2,6),(3,6)]
treasure_positions = [(7,7)]
terminate_states = [(4,5)]

map = Map(8,8, wall_positions,treasure_positions,terminate_states)

# Print the map for checking
def checking_map():
    for row in range(map_height):
        for column in range(map_length):
            print(grid[column][row].type, end=" ")
        print('')

# SARSA ALgorithm
# Build a q-value look up dictionary.
# Random initialise the q-value table.
# E.g. print(grid[2][1].east)
def q_learning():
    # Cumulate the terminal state positions for all runs
    terminal_at_treasure = 0
    terminal_at_end = 0

    # For each episode
    for episode in range(10000):

        # print('Episode %i'%episode)

        # Initialise the start state.
        start_x = random.randint(0,7)
        start_y = random.randint(0,7)

        # if episode == 99:
        # print('X Position: {} . Y Position: {}.'.format(start_x,start_y))
        # print(start_x,start_y)
        next_x = start_x
        next_y = start_y

        # Make sure the start state is not wall or treasure or terminate
        if grid[next_x][next_x].type == "wall":
            continue
        elif grid[next_x][next_x].type == "treasure":
            continue
        elif grid[next_x][next_x].type == "terminate":
            continue

        step = 0
        # For each episode step, only stops if the agent reached the treasure or terminate.
        while grid[next_x][next_y].type != "terminate" and grid[next_x][next_y].type !="treasure":

            # Choose an action a from given policy, here is the e-greedy policy
            action = e_greedy_action(next_x, next_y)
            # print(action)

            # print("Step {}: {}. (x,y)=({},{})".format(step, action, next_x, next_y))
            step+=1
            adjust = calculate_adjustment(action)
            outofbound = check_out_of_bound(next_x+adjust[0],next_y+adjust[1])
            if outofbound:
                # Perform the action and observe the r and s'
                action_reward = -10
                current_state = grid[next_x][next_y]
                next_state = grid[next_x][next_y]
                # Choose a' from s' using policy derive from Q
                next_action = random_action()
                while next_action == action:
                    next_action = random_action()

                next_state_action_value = -1

                # Q(s,a) += alpha * (r + gamma * Q(s', a') - Q(s,a))
                if action == 'east':
                    grid[next_x][next_y].east += learning_rate * (
                        action_reward + discounting_factor * next_state_action_value - current_state.east)
                elif action == 'west':
                    grid[next_x][next_y].west += learning_rate * (
                        action_reward + discounting_factor * next_state_action_value - current_state.west)
                elif action == 'south':
                    grid[next_x][next_y].south += learning_rate * (
                        action_reward + discounting_factor * next_state_action_value - current_state.south)
                else:
                    grid[next_x][next_y].north += learning_rate * (
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
                    current_state.east += learning_rate * (action_reward + discounting_factor * next_state_action_value - current_state.east)
                elif action == 'west':
                    current_state.west += learning_rate * (action_reward + discounting_factor * next_state_action_value - current_state.west)
                elif action == 'south':
                    current_state.south += learning_rate * (action_reward + discounting_factor * next_state_action_value - current_state.south)
                else:
                    current_state.north += learning_rate*(action_reward + discounting_factor*next_state_action_value - current_state.north)

                # state = next_state, action = next_action
                action = next_action
        # Summerise all the terminate results
        if episode > 0:
            if(grid[next_x][next_y].type == "terminate"):
                terminal_at_end += 1
            elif (grid[next_x][next_y].type == "treasure"):
                terminal_at_treasure += 1
            else:
                continue
        # print("Step {}: {}. (x,y)=({},{})".format(step, action, next_x, next_y))
        # print("Terminate at the end {} times.".format(terminal_at_end))
        # print("Terminate at the treasure {} times.".format(terminal_at_treasure))
    # Print the map for checking
    for row in range(map_height):
        for column in range(map_length):
            optimal_action = greedy_action(column, row)
            print(optimal_action,end = ' ')
        print('')


def main():
    q_learning()

if __name__ =="__main__":
    main()
