import random 
import copy

#Student name & surname: Eren Demircan
#Student ID: 2237246

# global variables and structures
# environment
M, N = 0, 0
obstacle_states = []
goal_states = []
reward = 0.0
learning_rate = 0.0
gamma = 0.0
epsilon = 0.0
episode_count = 0

# states as dict
states = dict()


# read file
def readFile(file_name):
    global M, N, obstacle_states, goal_states, reward, learning_rate, gamma, epsilon, episode_count, start_state, action_noise
    with open(file_name, 'r') as f:    
        lines = f.readlines()
        env = lines[1].split(' ')                                           # environment
        M = int(env[0])
        N = int(env[1])
        for i in range(M):
            for j in range(N):
                states.update({f"({i},{j})": 0.0})

        obs = lines[3][:-1]                                                 # obstacle states
        obstacles = obs.split('|')
        for obstacle in obstacles:
            obstacle_states.append(obstacle)
            states.update({obstacle: 0.0})
        
        goals = lines[5][:-1].split('|')                                    # goal states
        for goal in goals:
            temp = goal.split(':')
            goal_states.append(temp[0])
            states.update({temp[0]: float(temp[1])})

        start_state = lines[7][:-1]                                         # start state
        reward = float(lines[9])                                            # reward
        action_noise = (float(lines[11]), float(lines[12]), float(lines[13])) # action noise
        
        learning_rate = float(lines[15])                                    # learning rate
        gamma = float(lines[17])                                            # gamma
        epsilon = float(lines[19])                                          # epsilon
        episode_count = int(lines[21])                                      # episode count  

    return


# add noise to the action
def add_action_noise(action):
    action_list = [action]
    if action == "^":
        action_list.insert(0, "<")
        action_list.append(">")
    elif action == ">":
        action_list.insert(0, "^")
        action_list.append("V")
    elif action == "V":
        action_list.insert(0, ">")
        action_list.append("<")
    elif action_list == "<":
        action_list.insert(0, "V")
        action_list.append("^")
    elif action == ".":
        print("At exit state")
    else:
        print("Wrong action Type")
    
    actual_action = random_module.choices(action_list, weights=[action_noise[1], action_noise[0], action_noise[2]])
    return actual_action


# randomly selects an action
def select_action():
    actions = ["^", ">", "<", "V"]
    action = actions[random_module.rand_int(0, 3)]

    return add_action_noise(action)


# checks if up action is possible
def go_up(first_dim, second_dim):
    up = str(f"({first_dim - 1},{second_dim})")
    if up not in obstacle_states and up in states.keys():
        return up
    else:
        return str(f"{first_dim},{second_dim}")


# checks if right action is possible
def go_right(first_dim, second_dim):
    right = str(f"({first_dim},{second_dim+1})")
    if right not in obstacle_states and up in states.keys():
        return right
    else:
        return str(f"{first_dim},{second_dim}")


# checks if down action is possible
def go_down(first_dim, second_dim):
    down = str(f"({first_dim + 1},{second_dim})")
    if down not in obstacle_states and down in states.keys():
        return down
    else:
        return str(f"{first_dim},{second_dim}")


# checks if left action is possible
def go_left(first_dim, second_dim):
    left = str(f"({first_dim},{second_dim - 1})")
    if left not in obstacle_states and up in states.keys():
        return left
    else:
        return str(f"{first_dim},{second_dim}")


# given the current state and action
# returns the new state
def next_state(current_state, action):
    s = current_state.split(",")
    
    first_dim = int(s[0][1:])
    second_dim = int(s[1][:-1])

    if action == "^":
        new_state = go_up(first_dim, second_dim)
    elif action == ">":
        new_state = go_up(first_dim, second_dim)
    elif action == "V":
        new_state = go_up(first_dim, second_dim)
    elif action == "<":
        new_state = go_up(first_dim, second_dim)
    return new_state


def calculate_utility():
    return


# behaves differently for TD(0) and Q-Learning
def simulate(if_td, ):
    # TD0 -> 
    # Q-learning ->
    
    for i in range(episode_count):
        if random_module.random() <= epsilon:
            selected_action = select_action()
        else:
            # choose the action maximizing the utility based on the algorithm
            pass

        state = next_state(current_state, selected_action)
        if state in goal_states:
            reward 
            calculate_utility()
            break
        else:
            reward
            calculate_utility()
            
    return


def SolveMDP(method_name, problem_file, seed = 123):
    global random_module
    random_module = random.seed(seed)
    
    """
    Your implementation goes here
    """
    
    if method_name == "TD(0)":
        pass
    elif method_name == "Q-learning":
        pass

    return U, policy

readFile("mdp1.txt")