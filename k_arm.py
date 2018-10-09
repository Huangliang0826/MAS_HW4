import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import boltzmann

def epsilon_greedy(epsilon):
    # Make random seed.
    np.random.seed(0)
    # Initialise two list: mu[] and sigma[]
    # mu and sigma are essential for normal distribution function.
    mu = []
    sigma = []
    records = []
    estimates = []
    reward_history = []
    current_sum = 0
    arm_num = 10
    for i in range (arm_num):
        mu.append(np.random.randint(-3,3))
        sigma.append(0.1)
        records.append([])
        estimates.append(0)
        print('mu value %i: %f.' %(i, mu[i]))
        print('sigma value %i: %f.' %(i,sigma[i]))

    # Make random number unpredictable.
    np.random.seed()

    ########################
    #Epsilon-Greedy Method##
    ########################

    # Calculate the estimate reward for each action
    for i in range(arm_num):
        estimates[i] = 0

    # Exploration and Exploitation for 9000 transactions
    # Need to balance those two factors.
    test_times = 2000
    eps = epsilon
    index = 0
    while index < test_times:
        if np.random.random_sample() > eps:
            action = estimates.index(max(estimates))
        else:
            action = np.random.randint(0, arm_num)
        # Update estimates
        reward = np.random.normal(mu[action], sigma[action])
        records[action].append(reward)
        current_sum += reward
        reward_history.append(current_sum/(index+1))
        if len(estimates) != 0:
            estimates[action] = estimates[action] + 1.0/len(estimates)*(reward - estimates[action])
        else:
            estimates[action] = 0
        index+=1

    # Calculate the estimate reward for each action
    for i in range(arm_num):
        print('Estimates: %i : %f' %(i,sum(records[i])))

    return reward_history


def optimistic_epsilon_greedy(epsilon):
    # Make random seed.
    np.random.seed(0)
    # Initialise two list: mu[] and sigma[]
    # mu and sigma are essential for normal distribution function.
    mu = []
    sigma = []
    records = []
    estimates = []
    reward_history = []
    current_sum = 0
    arm_num = 10
    for i in range (arm_num):
        mu.append(np.random.randint(-3,3))
        sigma.append(0.1)
        records.append([])
        estimates.append(0)
        print('mu value %i: %f.' %(i, mu[i]))
        print('sigma value %i: %f.' %(i,sigma[i]))

    # Make random number unpredictable.
    np.random.seed()

    ########################
    #Epsilon-Greedy Method##
    ########################

    # Calculate the estimate reward for each action
    for i in range(arm_num):
        estimates[i] = 10

    # Exploration and Exploitation for 2000 transactions
    # Need to balance those two factors.
    test_times = 2000
    eps = epsilon
    index = 0
    while index < test_times:
        if np.random.random_sample() > eps:
            action = estimates.index(max(estimates))
        else:
            action = np.random.randint(0, arm_num)
        # Update estimates
        reward = np.random.normal(mu[action], sigma[action])
        records[action].append(reward)
        current_sum += reward
        reward_history.append(current_sum/(index+1))
        if len(estimates) != 0:
            estimates[action] = estimates[action] + 1.0/len(estimates)*(reward - estimates[action])
        else:
            estimates[action] = 0
        index+=1

    # Calculate the estimate reward for each action
    for i in range(arm_num):
        print('Estimates: %i : %f' %(i,sum(records[i])))

    return reward_history


times = np.arange(0,2000, 1)
plt.figure(figsize=(10,5))
plt.title('10 armed bandits: E-Greedy vs E-Greedy with optimistic initialisation')
# plot epsilon greedy method results
reward_his_1 = epsilon_greedy(0.1)
reward_his_1_5 = epsilon_greedy(0.15)
reward_his_2 = epsilon_greedy(0.2)
reward_his_2_5 = epsilon_greedy(0.25)
reward_his_3 = epsilon_greedy(0.3)

avg_reward_epsilon = np.array([reward_his_1,reward_his_1_5,reward_his_2,reward_his_2_5, reward_his_3])
avg_reward_epsilon = np.mean(avg_reward_epsilon, axis=0)

plt.plot(times, avg_reward_epsilon,linewidth=0.7)

reward_opt_1 = optimistic_epsilon_greedy(0.1)
reward_opt_1_5 = optimistic_epsilon_greedy(0.15)
reward_opt_2 = optimistic_epsilon_greedy(0.2)
reward_opt_2_5 = optimistic_epsilon_greedy(0.25)
reward_opt_3 = optimistic_epsilon_greedy(0.3)

avg_reward_optimiatic_epsilon = np.array([reward_opt_1,reward_opt_1_5,reward_opt_2,reward_opt_2_5, reward_opt_3])
avg_reward_optimiatic_epsilon = np.mean(avg_reward_optimiatic_epsilon, axis=0)

plt.plot(times, avg_reward_optimiatic_epsilon,linewidth=0.7)

plt.legend(['Ɛ-Greedy Ɛ = 0.1~0.3','Ɛ-Greedy with optimistic initialisation Ɛ = 0.1~0.3, Initial expectation value = 10'])
plt.xlabel('Steps')
plt.ylabel('Average Rewards')
plt.show()
