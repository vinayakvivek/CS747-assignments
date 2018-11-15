import argparse
from glob import glob
import os
import numpy as np
import csv
from utils import PLOT_DIR
import matplotlib.pyplot as plt


def plot(log_dir):
    os.makedirs(PLOT_DIR, exist_ok=True)
    log_files = sorted(glob(os.path.join(log_dir, '*')))

    # print(log_dir)

    with open(log_files[0], 'r') as f:
        reader = csv.reader(f, delimiter=',')
        num_episodes = len(list(reader))

    time_steps = np.zeros(num_episodes)

    for file_path in log_files:
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for i, row in enumerate(reader):
                time_steps[i] += float(row[2])

    time_steps = time_steps / len(log_files)

    env_name = os.path.basename(log_dir.strip('/'))
    plot_name = "%s.png" % (env_name)
    plt.plot(time_steps, [x+1 for x in range(num_episodes)])
    plt.xlabel('Time steps')
    plt.ylabel('Episodes')
    plt.savefig(os.path.join(PLOT_DIR, plot_name))
    print('plot saved at `%s`' % (os.path.join(PLOT_DIR, plot_name)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SARSA experiment plotter')
    parser.add_argument('--logdir',
                        metavar='E',
                        required=True,
                        help='path to experiment logs')
    args = parser.parse_args()

    plot(args.logdir)
