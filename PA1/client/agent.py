import socket
import argparse
import logging
import numpy as np
import math
import csv
import sys


logging.basicConfig(
    format='[%(levelname)s][%(asctime)s]: %(message)s',
    level=logging.ERROR
)


class BanditAgent():

    def __init__(self, args):
        logging.info('initializing bandit agent..')
        self.num_arms = args.numArms
        self.random_seed = args.randomSeed
        self.horizon = args.horizon
        self.hostname = args.hostname
        self.port = args.port

        self.total_pulls = 0
        self.pull_history = []
        self.reward_history = []

        self.arm_values = [0.0] * self.num_arms
        self.arm_counts = [0] * self.num_arms

    def connect_to_server(self):
        logging.debug('connecting to server: %s:%d' % (self.hostname, self.port))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((self.hostname, self.port))
        except Exception as e:
            print('connection problem.')
            self.client_socket.close()
            sys.exit(1)

    def close_connection(self):
        self.client_socket.close()

    def sample_arm(self):
        """
        abstract method: should be implemented in subclass
        """
        raise NotImplementedError("Subclasses should implement this!")

    def pull_arm(self):
        """
        select an arm and send it's ID to server.
        receive reward from server and update history
        """
        arm_id = self.sample_arm()

        self.client_socket.send(str(arm_id).encode())
        data = self.client_socket.recv(256).decode()

        try:
            reward = float(data.split(',')[0])
        except Exception as e:
            print('\n' + str(e), 'arm_id:', arm_id)
            return

        self.update(arm_id, reward)

    def update(self, arm_id, reward):
        self.total_pulls += 1
        self.pull_history.append(arm_id)
        self.reward_history.append(reward)

        logging.debug('pull %d - arm: %d, reward: %f' % (self.total_pulls, arm_id, reward))

        # increment pull count of the arm pulled just now
        self.arm_counts[arm_id] += 1
        n = self.arm_counts[arm_id]

        # update empirical mean
        self.arm_values[arm_id] = ((n - 1) * self.arm_values[arm_id] + reward) / float(n)

    def run(self):
        """
        run bandit till horizon
        """
        self.connect_to_server()

        while self.total_pulls < self.horizon:
            self.pull_arm()

        # arm_id = self.sample_arm()
        # while self.client_socket.send(str(arm_id).encode()) > 0:
        #     data = self.client_socket.recv(256).decode()
        #     reward = float(data.split(',')[0])
        #     self.update(arm_id, reward)
        #     arm_id = self.sample_arm()

        self.close_connection()

    def save_history(self, file_name):
        """
        save reward history into a csv file
        """
        with open(file_name, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for i in range(self.total_pulls):
                writer.writerow([self.pull_history[i], self.reward_history[i]])


class RoundRobinAgent(BanditAgent):

    def __init__(self, args):
        super(RoundRobinAgent, self).__init__(args)

    def sample_arm(self):
        return self.total_pulls % self.num_arms


class EpsilonGreedyAgent(BanditAgent):

    def __init__(self, args):
        super(EpsilonGreedyAgent, self).__init__(args)
        self.epsilon = args.epsilon

    def sample_arm(self):
        p = np.random.uniform()
        if p < self.epsilon:
            # explore uniformly at random
            return np.random.randint(0, self.num_arms)
        else:
            # pull arm with highest empirical mean
            return np.argmax(self.arm_values)


class UCBAgent(BanditAgent):

    def __init__(self, args):
        super(UCBAgent, self).__init__(args)

    def sample_arm(self):
        # pull each arm once
        if self.total_pulls < self.num_arms:
            return self.total_pulls

        ucb_values = [0.0] * self.num_arms

        for i in range(self.num_arms):
            confidence_term = math.sqrt((2 * math.log(self.total_pulls)) / self.arm_counts[i])
            ucb_values[i] = self.arm_values[i] + confidence_term

        return np.argmax(ucb_values)


def kl(x, y):
    t1 = 0
    try:
        t1 = x * math.log(x / y)
    except Exception as e:
        # print('t1', x, y)
        pass

    t2 = 0
    try:
        t2 = (1 - x) * math.log((1 - x) / (1 - y))
    except Exception as e:
        # print('t2', x, y)
        pass

    return t1 + t2


class KLUCBAgent(BanditAgent):

    def __init__(self, args):
        super(KLUCBAgent, self).__init__(args)
        logging.info('initialized KL-UCB agent.')
        self.tolerance = 1e-6

    def kl_upper_bound(self, arm_id):
        u = self.arm_counts[arm_id]
        t = self.total_pulls
        return (math.log(t) + 3 * math.log(math.log(t))) / u
        # return math.log(t) / u

    def ucb(self, arm_id):
        upper_bound = self.kl_upper_bound(arm_id)
        p_a = self.arm_values[arm_id]

        # binary search
        low = p_a
        high = 1
        mid = (low + high) / 2
        while abs(low - high) > self.tolerance:
            mid = (low + high) / 2
            if kl(p_a, mid) <= upper_bound:
                low = mid
            else:
                high = mid

        # print(kl(p_a, mid), upper_bound, mid, self.arm_counts[arm_id], self.total_pulls)
        return mid

    def sample_arm(self):
        # pull each arm once
        if self.total_pulls < self.num_arms:
            return self.total_pulls

        ucb_values = [0.0] * self.num_arms

        for i in range(self.num_arms):
            ucb_values[i] = self.ucb(i)

        # max_arm = np.argmax(ucb_values)
        # print(max_arm, self.arm_values[max_arm])
        return np.argmax(ucb_values)


class ThompsonSamplingAgent(BanditAgent):

    def __init__(self, args):
        super(ThompsonSamplingAgent, self).__init__(args)
        self.arm_success_counts = [0] * self.num_arms
        self.arm_failure_counts = [0] * self.num_arms

    def sample_arm(self):
        # sample each x from each arm's beta distribution
        sample_values = []
        for i in range(self.num_arms):
            a = self.arm_success_counts[i] + 1
            b = self.arm_failure_counts[i] + 1
            sample_values.append(np.random.beta(a, b))
        return np.argmax(sample_values)

    def update(self, arm_id, reward):
        super(ThompsonSamplingAgent, self).update(arm_id, reward)

        # do a Bernoulli trial with reward as success prob
        p = np.random.uniform()
        if p < reward:
            # success
            self.arm_success_counts[arm_id] += 1
        else:
            self.arm_failure_counts[arm_id] += 1


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Bandit agent args.')
    parser.add_argument('--numArms', metavar='N', help='number of arms of the bandit.', type=int, default=5)
    parser.add_argument('--randomSeed', metavar='R', help='seed for generating random nums.', type=int, default=0)
    parser.add_argument('--horizon', metavar='T', help='how long should the bandit run.', type=int, default=200)
    parser.add_argument('--hostname', metavar='<ip>', help='address of host/server', type=str, default='localhost')
    parser.add_argument('--port', metavar='p', help='server port number.', type=int, default=5000)
    parser.add_argument('--algorithm', metavar='A', help='bandit algorithm', type=str, default='rr')
    parser.add_argument('--epsilon', metavar='e', help='small positive value', type=float, default=0.0)

    args = parser.parse_args()

    if args.algorithm == 'rr':
        agent = RoundRobinAgent(args)
    elif args.algorithm == 'epsilon-greedy':
        agent = EpsilonGreedyAgent(args)
    elif args.algorithm == 'UCB':
        agent = UCBAgent(args)
    elif args.algorithm == 'KL-UCB':
        agent = KLUCBAgent(args)
    elif args.algorithm == 'Thompson-Sampling':
        agent = ThompsonSamplingAgent(args)

    agent.run()
    # agent.save_history('../client_log.csv')
