import json
from enum import Enum
from copy import deepcopy
import logging
from utils import W, N, E, S


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
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

        self.length = data["size"][0]
        self.breadth = data["size"][1]
        self.king_move = data["king_move"]

        self.start = data["start"]
        self.goal = data["goal"]
        self.wind = data["wind"]

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

        if action == W and self.curr_state[0] > 0:
            next_state[0] -= 1
        elif action == N and (self.curr_state[0] + 1) < self.length:
            next_state[0] += 1
        elif action == E and self.curr_state[1] > 0:
            next_state[1] -= 1
        elif action == S and (self.curr_state[1] + 1) < self.breadth:
            next_state[1] += 1

        curr_wind = self.wind[self.curr_state[0]]
        next_state[1] = min(next_state[1] + curr_wind, self.breadth-1)

        reward = -1

        if next_state == self.goal:
            reward = 0
            self.done = True

        self.curr_state = next_state
        self.num_steps += 1
        self.history.append(self.curr_state)

        return (next_state, reward, self.done)

    def reset(self):
        self.curr_state = self.start
        self.history = [self.curr_state]
        self.num_steps = 0
        self.done = False
        return self.curr_state


if __name__ == '__main__':
    env_file = 'sample_env.json'
    env = WindyGrid(env_file)

    print(LEFT)

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
