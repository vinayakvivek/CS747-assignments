import argparse
import matplotlib.pyplot as plt
import os


def plot_policy(file_path):

    with open(file_path, 'r') as f:
        lines = f.readlines()

    ph = os.path.splitext(os.path.basename(file_path))[0].split('_')[-1]
    ph = ''.join(ph.split('.'))

    lines = [x.strip() for x in lines]
    policy = [int(x.split('\t')[1]) for x in lines]
    values = [float(x.split('\t')[0]) for x in lines]
    # print(policy)

    plt.figure()
    plt.step([x for x in range(1, len(policy)-1)], policy[1:-1])
    plt.xlabel('Capital')
    plt.ylabel('Final policy')
    plt.savefig('./plots/policy_%s.png' % (ph))

    plt.figure()
    plt.plot(values[1:-1])
    plt.xlabel('Capital')
    plt.ylabel('Value Estimate')
    plt.savefig('./plots/values_%s.png' % (ph))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gambler problem graph plotter.')
    parser.add_argument('-f',
                        '--policy',
                        metavar='file_path',
                        help='absolute path to policy file')
    args = parser.parse_args()

    plot_policy(args.policy)
