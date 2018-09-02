import csv
import matplotlib.pyplot as plt
import codecs
import os
import numpy as np
from glob import glob


# instance = 'betaDist_5'
# horizon = 1000

# MAIN_LOG_DIR = '../logs/%s_%d' % (instance, horizon)
# subdirs = sorted(glob(MAIN_LOG_DIR + '/*'))

main_out_dir = '../client/logs/'
os.makedirs(main_out_dir, exist_ok=True)

data_dir = '../logs/'
instance_dirs = sorted(glob(os.path.join(data_dir, '*')))

for k, instance in enumerate(instance_dirs):

    out_dir = os.path.join(main_out_dir, os.path.basename(instance))
    os.makedirs(out_dir, exist_ok=True)

    subdirs = sorted(glob(os.path.join(instance, '*')))

    print(k, os.path.basename(instance))

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

        print('\t', index, os.path.basename(algo), num_runs)

        average_rewards /= num_runs

        max_mean = float(lines[-3][0].split('maxMean')[1])

        cumulative_regrets = []

        t = max_mean - average_rewards[0]
        cumulative_regrets.append(t)

        for i in range(1, len(average_rewards)):
            t += (max_mean - average_rewards[i])
            cumulative_regrets.append(t)

        save_path = os.path.join(out_dir, os.path.basename(algo) + '.csv')
        with open(save_path, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['reward', 'cumulative_regret'])
            for i in range(len(average_rewards)):
                writer.writerow([average_rewards[i], cumulative_regrets[i]])
