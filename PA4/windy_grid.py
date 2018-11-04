import json
from enum import Enum
from copy import deepcopy


class Action(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


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
        self.max_steps = int(data["max_steps"])

        self.start = data["start"]
        self.goal = data["goal"]
        self.wind = data["wind"]

        self.reset()

    def step(self, action):
        """
        take action from current state
        return next state, reward, "done" (and "info" if required)
        """
        if self.done:
            return (self.curr_state, 0, self.done)

        next_state = deepcopy(self.curr_state)

        if action == Action.LEFT and self.curr_state[0] > 0:
            next_state[0] -= 1
        elif action == Action.RIGHT and (self.curr_state[0] + 1) < self.length:
            next_state[0] += 1
        elif action == Action.DOWN and self.curr_state[1] > 0:
            next_state[1] -= 1
        elif action == Action.UP and (self.curr_state[1] + 1) < self.breadth:
            next_state[1] += 1

        curr_wind = self.wind[self.curr_state[0]]
        next_state[1] = min(next_state[1] + curr_wind, self.breadth)

        reward = -1

        if next_state == self.goal:
            reward = 0
            self.done = True

        self.curr_state = next_state
        self.num_steps += 1

        if self.num_steps >= self.max_steps:
            self.done = True

        return (next_state, reward, self.done)

    def reset(self):
        self.curr_state = self.start
        self.num_steps = 0
        self.done = False


if __name__ == '__main__':
    env_file = 'sample_env.json'
    env = WindyGrid(env_file)

    for i in range(9):
        s, r, d = env.step(Action.RIGHT)
        print(s, r, d)

    for i in range(5):
        s, r, d = env.step(Action.DOWN)
        print(s, r, d)

    for i in range(2):
        s, r, d = env.step(Action.LEFT)
        print(s, r, d)

    for i in range(5):
        s, r, d = env.step(Action.UP)
        print(s, r, d)
