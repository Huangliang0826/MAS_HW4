import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import boltzmann

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
epsilon = 0.2
index = 0
while index < test_times:
    if np.random.random_sample() > epsilon:
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

times = np.arange(0,2000, 1)
plt.plot(times, reward_history)
plt.show()
