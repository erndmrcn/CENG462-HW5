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


def SolveMDP(method_name, problem_file, seed = 123):
    random.seed(seed)
    
    """
    Your implementation goes here
    """
    
    if method_name == "TD(0)":
        pass
    elif method_name == "Q-learning":
        pass

    return U, policy

readFile("mdp1.txt")