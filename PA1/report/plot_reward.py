import csv
import matplotlib.pyplot as plt
import codecs
import os
import numpy as np
import progressbar
from glob import glob

# exp_data = {
#     'algorithm': 'KL-UCB',
#     'horizon': 1000,
#     'epsilon': 0.30,
#     'instance': 'betaDist_5'
# }

# if exp_data['algorithm'] == 'epsilon-greedy':
#     LOG_DIR = '../logs/%s_%d/%s_%0.2f' % (
#         exp_data['instance'],
#         exp_data['horizon'],
#         exp_data['algorithm'],
#         exp_data['epsilon'])
# else:
#     LOG_DIR = '../logs/%s_%d/%s' % (
#         exp_data['instance'],
#         exp_data['horizon'],
#         exp_data['algorithm'])


# instance = 'betaDist_25'
# instance = 'instance-bernoulli-25'
instance = 'instance-histogram-25'
horizon = 10000

MAIN_LOG_DIR = '../logs/%s_%d' % (instance, horizon)
subdirs = sorted(glob(MAIN_LOG_DIR + '/*'))

num_runs = 100

for index, algo in enumerate(subdirs):

    average_rewards = None
    file_paths = sorted(glob(os.path.join(algo, '*')))
    num_runs = 0

    for file_path in file_paths:
        reward_list = []
        lines = []
        file_size = os.stat(file_path).st_size

        if file_size == 0:
            continue

        with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        lines = [x.strip().rstrip('\n').split() for x in lines]
        for line in lines:
            if len(line) > 0 and line[0] == 'S':
                # get reward
                reward_list.append(float(line[1]))

        if average_rewards is None:
            average_rewards = np.array(reward_list)
        else:
            average_rewards += np.array(reward_list)

        num_runs += 1

    print(index, os.path.basename(algo), num_runs)

    average_rewards /= num_runs

    max_mean = float(lines[-3][0].split('maxMean')[1])
    # print('#pulls:', len(reward_list), ', max_mean:', max_mean)

    cumulative_regrets = []

    t = max_mean - average_rewards[0]
    cumulative_regrets.append(t)

    for i in range(1, len(average_rewards)):
        t += (max_mean - average_rewards[i])
        cumulative_regrets.append(t)

    plt.plot(cumulative_regrets, label=os.path.basename(algo))

plt.ylabel('regret')
plt.xlabel('number of pulls')
title = '%s_%d' % (instance, horizon)
plt.title(title)
plt.legend()
plt.savefig('./plots/' + title + '.png')

# if exp_data['algorithm'] == 'epsilon-greedy':
#     plt.title('algo: %s | ε: %0.2f | instance: %s' % (
#         exp_data['algorithm'],
#         exp_data['epsilon'],
#         exp_data['instance']))
# else:
#     plt.title('algo: %s | instance: %s' % (
#         exp_data['algorithm'],
#         exp_data['instance']))

# save_dir = 'plots/' + os.path.dirname(LOG_DIR)
# os.makedirs(save_dir, exist_ok=True)
# plt.savefig('%s/%s.png' % (save_dir, os.path.basename(LOG_DIR)))
# plt.close()