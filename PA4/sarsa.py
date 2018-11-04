from windy_grid import WindyGrid
from pprint import pprint
import numpy as np
import logging
from copy import deepcopy
from utils import LEFT, RIGHT, DOWN, UP


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt='[%(levelname)s][%(asctime)s]: %(message)s',
    datefmt='%H:%M:%S'
)
ch.setFormatter(formatter)

logger.addHandler(ch)


class SarsaAgent:

    def __init__(self, env, alpha, gamma, epsilon):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.num_states = self.env.length * self.env.breadth
        self.Q = dict([(x, [0, 0, 0, 0]) for x in range(self.num_states)])

    def _decode_state(self, state):
        return (state[1] * self.env.length + state[0])

    def _get_action(self, state):
        e = np.random.random_sample()
        if e > self.epsilon:
            return np.argmax(self.Q[self._decode_state(state)])
        else:
            logger.debug("exploring: random action")
            return np.random.choice(4, 1)[0]

    def _run_episode(self):
        state = self.env.reset()
        action = self._get_action(state)

        prev_state = None
        prev_action = None
        done = False

        while not done:
            state, reward, done = self.env.step(action)
            logger.debug("state: %s, reward: %f, done: %s" % (str(state), reward, str(done)))
            action = self._get_action(state)

            if prev_state is not None:
                q_old = self.Q[self._decode_state(prev_state)][prev_action]
                q_new = q_old
                if done:
                    q_new += self.alpha * (reward - q_old)
                else:
                    q_new += self.alpha * (reward + self.gamma * self.Q[self._decode_state(state)][action] - q_old)

                self.Q[self._decode_state(prev_state)][prev_action] = q_new

            prev_state = state
            prev_action = action

    def run(self, num_episodes=100):
        time_steps = 0
        for i in range(num_episodes):
            self._run_episode()
            time_steps += self.env.num_steps
            logger.info("episode: %d, steps: %d, total_time: %d" % (i + 1, self.env.num_steps, time_steps))


if __name__ == '__main__':

    env_file = 'sample_env.json'
    env = WindyGrid(env_file)
    agent = SarsaAgent(env, 0.5, 1, 0.01)

    agent.run(200)
