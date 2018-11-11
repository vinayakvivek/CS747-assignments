from windy_grid import WindyGrid
import numpy as np
import logging
import matplotlib.pyplot as plt
from copy import deepcopy
import argparse
import os
import sys
from utils import PLOT_DIR, LOG_DIR, LOG_LEVEL


logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logger(args):
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(
        logging.Formatter(
            fmt='[%(levelname)s][%(asctime)s]: %(message)s',
            datefmt='%H:%M:%S'
        ))
    logger.addHandler(ch)

    os.makedirs(args.logdir, exist_ok=True)
    file_name = os.path.join(args.logdir, str(args.seed) + ".csv")
    if os.path.exists(file_name):
        os.remove(file_name)

    fh = logging.FileHandler(filename=file_name)
    fh.setLevel(LOG_LEVEL)
    fh.setFormatter(logging.Formatter(fmt='%(message)s'))
    logger.addHandler(fh)


class SarsaAgent:

    def __init__(self, env, alpha, gamma, epsilon, seed):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.seed = seed

        self.num_states = self.env.get_num_states()
        self.num_actions = self.env.get_num_actions()
        self.Q = dict([(x, [0 for a in range(self.num_actions)])
                       for x in range(self.num_states)])
        np.random.seed(seed)

    def _decode_state(self, state):
        return (state[1] * self.env.length + state[0])

    def _get_action(self, state):
        e = np.random.random_sample()
        if e > self.epsilon:
            return np.argmax(self.Q[self._decode_state(state)])
        else:
            logger.debug("exploring: random action")
            return np.random.choice(self.num_actions, 1)[0]

    def _run_episode(self):
        state = self.env.reset()
        action = self._get_action(state)

        prev_state = None
        prev_action = None
        done = False

        while not done:
            state, reward, done = self.env.step(action)
            logger.debug("state: %s, reward: %f, done: %s" % (
                str(state), reward, str(done)))
            action = self._get_action(state)

            if prev_state is not None:
                q_old = self.Q[self._decode_state(prev_state)][prev_action]
                q_new = q_old
                if done:
                    q_new += self.alpha * (reward - q_old)
                else:
                    q_new += self.alpha * (
                        reward +
                        self.gamma * self.Q[self._decode_state(state)][action]
                        - q_old)

                self.Q[self._decode_state(prev_state)][prev_action] = q_new

            prev_state = state
            prev_action = action

    def run(self, num_episodes=100):
        time_steps = []
        episodes = []
        total_time = 0

        min_steps = 100
        min_step_move = None

        # print('')

        for i in range(num_episodes):
            self._run_episode()
            total_time += self.env.num_steps
            time_steps.append(total_time)
            episodes.append(i + 1)

            if self.env.num_steps <= min_steps:
                min_steps = self.env.num_steps
                min_step_move = deepcopy(self.env.history)

            logger.info("%d, %d, %d" % (i + 1, self.env.num_steps, total_time))

            sys.stdout.write("\rrunning episode: %d/%d" % (i + 1, num_episodes))
            sys.stdout.flush()

        # print('\n')
        # print("minimum number of steps: %d\n" % (min_steps))
        # print("best path (list of (action, next-state)):\n %s\n" % (str(min_step_move)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SARSA experiment')
    parser.add_argument('--env',
                        metavar='E',
                        required=True,
                        help='path to environment description file')
    parser.add_argument('--logdir',
                        metavar='L',
                        help='log directory',
                        type=str,
                        required=True)
    parser.add_argument('--alpha',
                        metavar='𝛼',
                        help='learning rate',
                        type=float,
                        default=0.5)
    parser.add_argument('--gamma',
                        metavar='𝛾',
                        help='discount factor',
                        type=float,
                        default=1)
    parser.add_argument('--epsilon',
                        metavar='𝜀',
                        help='exploration rate',
                        type=float,
                        default=0.01)
    parser.add_argument('--seed',
                        metavar='r',
                        help='random seed',
                        type=int,
                        default=1)
    parser.add_argument('--episodes',
                        metavar='N',
                        help='number of episodes to run',
                        type=int,
                        default=200)

    args = parser.parse_args()

    setup_logger(args)

    env_file = args.env
    env = WindyGrid(env_file)
    agent = SarsaAgent(env, args.alpha, args.gamma, args.epsilon, args.seed)

    agent.run(args.episodes)
