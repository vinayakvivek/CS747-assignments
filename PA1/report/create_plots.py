import csv
import matplotlib.pyplot as plt
import os
from glob import glob


data_dir = '../client/logs/'
instance_dirs = sorted(glob(os.path.join(data_dir, '*')))

for k, instance in enumerate(instance_dirs):

    instance_name = os.path.basename(instance)
    print(k, instance_name)
    run_files = sorted(glob(os.path.join(instance, '*')))

    plt.figure()

    for run_file in run_files:

        cumulative_regrets = []
        with open(run_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for row in reader:
                cumulative_regrets.append(row[1])

        plt.plot(cumulative_regrets, label=os.path.splitext(os.path.basename(run_file))[0])

    xlim = 1000
    ylim = 300
    if int(instance.split('_')[-1]) == 10000:
        xlim = 10000
        ylim = 1500

    plt.axis((0, xlim, 0, ylim))
    plt.ylabel('cumulative regret')
    plt.xlabel('number of pulls')
    title = instance_name
    plt.title(title)
    plt.legend()
    plt.savefig('./plots/' + title + '.png')