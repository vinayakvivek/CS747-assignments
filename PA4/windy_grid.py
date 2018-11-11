import json
from copy import deepcopy
import logging
from utils import W, N, E, S, NE, NW, SE, SW
import numpy as np
from utils import LOG_LEVEL, num_to_dir


logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
formatter = logging.Formatter(
    fmt='[%(levelname)s][%(asctime)s]: %(message)s',
    datefmt='%H:%M:%S'
)
ch.setFormatter(formatter)

logger.addHandler(ch)


class WindyGrid:

    def __init__(self, env_file):
        self.env_file = env_file
        self.initialize(env_file)

    def initialize(self, env_file):
        """
        read env file and initialize attributes
        """
        with open(env_file) as f:
            data = json.load(f)

        logger.info('initilizing Windy GridWorld..')

        self.length = data["size"][0]
        self.breadth = data["size"][1]
        self.king_move = data["king_move"]
        self.stochastic = data["stochastic"]

        self.start = data["start"]
        self.goal = data["goal"]
        self.wind = data["wind"]

        logger.info('size: (%d, %d)' % (self.length, self.breadth))
        logger.info('king\'s move allowed?: %r' % (self.king_move))
        logger.info('stochastic wind?: %r' % (self.stochastic))

        self.reset()

    def get_num_states(self):
        return self.length * self.breadth

    def get_num_actions(self):
        if not self.king_move:
            return 4
        else:
            return 8

    def step(self, action):
        """
        take action from current state
        return next state, reward, "done" (and "info" if required)
        """
        if self.done:
            return (self.curr_state, 0, self.done)

        logger.debug("step @ state: %s, action: %d" % (str(self.curr_state), action))

        next_state = deepcopy(self.curr_state)

        if action == W:
            next_state[0] = self.curr_state[0] - 1
        elif action == E:
            next_state[0] = self.curr_state[0] + 1
        elif action == N:
            next_state[1] = self.curr_state[1] + 1
        elif action == S:
            next_state[1] = self.curr_state[1] - 1

        if self.king_move:
            if action == NW:
                next_state[0] = self.curr_state[0] - 1
                next_state[1] = self.curr_state[1] + 1
            elif action == NE:
                next_state[0] = self.curr_state[0] + 1
                next_state[1] = self.curr_state[1] + 1
            elif action == SE:
                next_state[0] = self.curr_state[0] + 1
                next_state[1] = self.curr_state[1] - 1
            elif action == SW:
                next_state[0] = self.curr_state[0] - 1
                next_state[1] = self.curr_state[1] - 1

        curr_wind = self.wind[self.curr_state[0]]
        if self.stochastic:
            curr_wind += (np.random.randint(3) - 1)

        next_state[1] = next_state[1] + curr_wind

        next_state[0] = np.clip(next_state[0], 0, self.length - 1)
        next_state[1] = np.clip(next_state[1], 0, self.breadth - 1)

        reward = -1

        if next_state == self.goal:
            reward = 0
            self.done = True

        self.curr_state = next_state
        self.num_steps += 1
        self.history.append((num_to_dir[action], self.curr_state))

        return (next_state, reward, self.done)

    def reset(self):
        self.curr_state = self.start
        self.history = [(None, self.curr_state)]
        self.num_steps = 0
        self.done = False
        return self.curr_state


if __name__ == '__main__':
    env_file = 'sample_env.json'
    env = WindyGrid(env_file)

    print(W)

    # for i in range(9):
    #     s, r, d = env.step(RIGHT)
    #     print(s, r, d)

    # for i in range(5):
    #     s, r, d = env.step(DOWN)
    #     print(s, r, d)

    # for i in range(2):
    #     s, r, d = env.step(LEFT)
    #     print(s, r, d)

    # for i in range(5):
    #     s, r, d = env.step(UP)
    #     print(s, r, d)
