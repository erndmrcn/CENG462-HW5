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
    if action == "<":
        action_list.insert(0, "V")
        action_list.append("^")
    elif action == "^":
        action_list.insert(0, "<")
        action_list.append(">")
    elif action == ">":
        action_list.insert(0, "^")
        action_list.append("V")
    elif action == "V":
        action_list.insert(0, ">")
        action_list.append("<")
    else:
        print("Wrong action Type")

    weights = [action_noise[1], action_noise[0], action_noise[2]]
    actual_action = random_module.choices(action_list, weights=weights)[0]
    return actual_action


# reset state dictionary
def reset_states():
    temp_states = copy.copy(states)
    for key in temp_states.keys():
        temp_states.update({key:float(0)})
    return temp_states


# randomly selects an action
def select_action():
    actions = ["<", "^", ">", "V"]
    action = actions[random_module.randint(0, 3)]
    return action


# checks if up action is possible
def go_up(first_dim, second_dim):
    up = str(f"({first_dim - 1},{second_dim})")
    if up not in obstacle_states and up in states.keys():
        return up
    else:
        return str(f"({first_dim},{second_dim})")


# checks if right action is possible
def go_right(first_dim, second_dim):
    right = str(f"({first_dim},{second_dim+1})")
    if right not in obstacle_states and right in states.keys():
        return right
    else:
        return str(f"({first_dim},{second_dim})")


# checks if down action is possible
def go_down(first_dim, second_dim):
    down = str(f"({first_dim + 1},{second_dim})")
    if down not in obstacle_states and down in states.keys():
        return down
    else:
        return str(f"({first_dim},{second_dim})")


# checks if left action is possible
def go_left(first_dim, second_dim):
    left = str(f"({first_dim},{second_dim - 1})")
    if left not in obstacle_states and left in states.keys():
        return left
    else:
        return str(f"({first_dim},{second_dim})")


# given the current state and action
# returns the new state
def next_state(current_state, action):
    s = current_state.split(",")
    
    first_dim = int(s[0][1:])
    second_dim = int(s[1][:-1])
    new_state = current_state
    if action == "<":
        new_state = go_left(first_dim, second_dim)
    elif action == "^":
        new_state = go_up(first_dim, second_dim)
    elif action == ">":
        new_state = go_right(first_dim, second_dim)
    elif action == "V":
        new_state = go_down(first_dim, second_dim)
    return new_state

k = 0
# chooses the action that maximizes the utility
# for TD(0), check neighbors and return the action that takes us to the max values neighbor
# for Q-learning, checks actions and returns the most valued action, and its value
def choose_action(if_td, local_states, current_state):
    actions = ["<", "^", ">", "V"]
    max_value = -float('inf')
    max_action = None

    if if_td == True:
        for action in actions:
            neighbor = next_state(current_state, action)
                
            if local_states[neighbor] > max_value:
                max_value = local_states[neighbor]
                max_action = action
        return max_action
    else:
        for action in actions:
            state = str(f"{current_state},{action}")
            if local_states[state] > max_value:
                max_value = local_states[state]
                max_action = action
        return max_value, max_action


# State action pair dictionary
# for Q-Learning
def learning_table():
    table = dict()
    actions = ["<", "^", ">", "V"]
    for state in states.keys():
        for action in actions:
            key = str(f"{state},{action}")
            table.update({key:float(0)})

    return table


# behaves differently for TD(0) and Q-Learning
def simulate(if_td):
    # TD0 -> initialize a value array
    if if_td:
        V = reset_states() 
    else:
        Q = learning_table()

    for i in range(episode_count):
        current_state = start_state

        while current_state not in goal_states:
            actual_action = None
            r = random_module.random()
        
            if r <= epsilon:
                selected_action = select_action()
                actual_action = add_action_noise(selected_action)
            else:
                # if TD(0)
                if if_td:
                    actual_action = add_action_noise(choose_action(if_td, V, current_state))
                # if Q-learning
                else:
                    selected_action = choose_action(if_td, Q, current_state)[1]
                    actual_action = add_action_noise(selected_action)

            state = next_state(current_state, actual_action)
            
            if state in goal_states:
                state_reward = reward + states[state]
                # update values
                if if_td:
                    V[current_state] = V[current_state] + learning_rate * (state_reward + gamma * V[state] - V[current_state])
                else:
                    key = str(f"{current_state},{selected_action}")
                    Q[key] = Q[key] + learning_rate * (state_reward + gamma * choose_action(if_td, Q, state)[0] - Q[key])
                break
            else:
                # update values
                if if_td:
                    V[current_state] = V[current_state] + learning_rate * (reward + gamma * V[state] - V[current_state])
                else:
                    key = str(f"{current_state},{selected_action}")
                    Q[key] = Q[key] + learning_rate * (reward + gamma * choose_action(if_td, Q, state)[0] - Q[key])
            
            current_state = state    
   
    if if_td:
        return V
    else:
        return Q


# modify result for correct output format Q-learning
def Qoutput(Q):
    value_result = dict()
    policy_result = dict()

    for key in Q.keys():
        splitted = key.split(',')
        state = splitted[0] + ',' + splitted[1]
        new_state = (int(splitted[0][1:]), int(splitted[1][:-1]))
        action = splitted[2]
        
        if state in obstacle_states or state in goal_states:
            continue

        value_result.update({new_state: round(choose_action(False, Q, state)[0] ,2)})
        policy_result.update({new_state: choose_action(False, Q, state)[1]})

    return value_result, policy_result


# arrange output for TD(0)
def TDoutput(V):
    value_result = dict()
    policy_result = dict()

    for state in goal_states:
        V[state] = states[state]

    for key in V.keys():
        splitted = key.split(",")

        new_state = (int(splitted[0][1:]), int(splitted[1][:-1]))
        
        if key in obstacle_states or key in goal_states:
            continue

        policy_result.update({new_state: choose_action(True, V, key)})
        value_result.update({new_state: round(V[key], 2)})

    for state in goal_states:
        V[state] = float(0)

    return value_result, policy_result


# reset values
def reset():
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

    return


def SolveMDP(method_name, problem_file, seed = 123):
    global random_module
    random_module = random
    random_module.seed(seed)
    
    reset()
    readFile(problem_file)

    if method_name == "TD(0)":
        result = TDoutput(simulate(True))
    elif method_name == "Q-learning":
        result = Qoutput(simulate(False))
    
    return result

# print(SolveMDP("Q-learning", "mdp3.txt", 462))