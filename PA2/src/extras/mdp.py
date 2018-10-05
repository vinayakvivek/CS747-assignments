import re
from copy import deepcopy
from pulp import LpProblem, LpMinimize, LpVariable,\
    LpStatus, value, LpStatusOptimal
import numpy as np
import argparse
import sys
import logging


logging.basicConfig(
    format='[%(levelname)s][%(asctime)s]: %(message)s',
    datefmt="%H:%M:%S",
    level=logging.ERROR
)


def clean_line(line):
    line = line.split()
    line = [float(x) for x in line]
    return line


class MDP():

    def __init__(self, S=0, A=0):
        """
        S (int): number of states
        A (int): number of actions
        """
        self.S = S
        self.A = A

    def read_from_file(self, file_path):

        lines = None
        with open(file_path, 'r') as f:
            lines = f.readlines()

        if lines is None:
            print('couldn\'t read MDP from %s' % (file_path))

        lines = [x.strip() for x in lines]
        self.S = int(lines[0])
        self.A = int(lines[1])

        self.rewards = [[None for a in range(self.A)] for s in range(self.S)]
        self.t_probs = [[None for a in range(self.A)] for s in range(self.S)]

        line_id = 2
        for s in range(self.S):
            for a in range(self.A):
                self.rewards[s][a] = deepcopy(clean_line(lines[line_id]))
                line_id += 1

        for s in range(self.S):
            for a in range(self.A):
                self.t_probs[s][a] = deepcopy(clean_line(lines[line_id]))
                line_id += 1

        self.discount = float(lines[line_id])
        self.type = lines[line_id + 1]

    def solve_LP(self):
        """
        solve MDP using linear programming methodxz
        """

        # create `prob` variable
        prob = LpProblem("MDP", LpMinimize)

        # create variables V(0), ..., V(S-1)
        V = []
        for s in range(self.S):
            x = LpVariable("V(%d)" % (s))
            V.append(x)

        # objective
        prob += sum(V), "sum_of_value_functions"

        # constraints
        for s in range(self.S):
            for a in range(self.A):
                c = sum([self.t_probs[s][a][x] * (self.rewards[s][a][x] + self.discount * V[x])\
                         for x in range(self.S)])
                prob += V[s] - c >= 0, "c_%d_%d" % (s, a)

        if self.type == 'episodic':
            # find terminal states
            for s in range(self.S):
                is_terminal = True
                for a in range(self.A):
                    for x in range(self.S):
                        if x != s and self.t_probs[s][a][x] > 0:
                            is_terminal = False
                            break
                    if not is_terminal:
                        break
                if is_terminal:
                    prob += V[s] == 0

        # # write problem to a .lp file
        # prob.writeLP("MDP.lp")

        # solve using PuLP's choice of Solver
        prob.solve()

        # The status of the solution is printed to the screen
        if not prob.status == LpStatusOptimal:
            print('could not find an optimal solution.')
            return

        # find optimal policy from value functions
        pi = []
        for s in range(self.S):
            values = []
            for a in range(self.A):
                values.append(
                        sum([self.t_probs[s][a][x] * (self.rewards[s][a][x] + self.discount * V[x].varValue)\
                            for x in range(self.S)])
                    )
            pi.append(np.argmax(values))

        self.values = [V[x].varValue for x in range(self.S)]
        self.pi = pi

    def _policy_eval(self, policy, eps=1e-6):
        """
        policy: policy[s] corresponds to action at state `s`
        """
        V = [0 for _ in range(self.S)]
        logging.debug('evaluating policy.')

        while True:
            delta = 0
            for s in range(self.S):
                a = policy[s]
                v = sum([self.t_probs[s][a][x] * (self.rewards[s][a][x] + self.discount * V[x])\
                        for x in range(self.S)])

                delta = max(delta, abs(v - V[s]))
                V[s] = v

            if delta < eps:
                break

        return V

    def solve_PI(self, max_iter=100, eps=1e-6):
        """
        solve MDP using policy iteration method
        """

        policy = [0 for _ in range(self.S)]  # initial policy
        V = [0 for _ in range(self.S)]
        iterations = 0
        # print('[iter %d]' % (iterations))

        while True and iterations < max_iter:
            policy_stable = True
            iterations += 1
            logging.info('iter: %d' % (iterations))
            improved_states = []

            # for s in range(self.S):
            #     a = policy[s]
            #     V[s] = sum([self.t_probs[s][a][x] * (self.rewards[s][a][x] + self.discount * V[x])\
            #                for x in range(self.S)])
            V = self._policy_eval(policy, eps)

            for s in range(self.S):
                q_best = V[s]
                for a in range(self.A):
                    q = sum([self.t_probs[s][a][x] * (self.rewards[s][a][x] + self.discount * V[x])\
                            for x in range(self.S)])
                    if q > q_best and abs(q - q_best) > eps:
                        improved_states.append((s, q_best, q))
                        policy[s] = a
                        q_best = q
                        policy_stable = False

            # logging.debug('improved_states: %s' % (str(improved_states)))

            if policy_stable:
                logging.debug('achieved a stable policy.')
                break

        self.values = V
        self.pi = policy

    def print(self):
        for s in range(self.S):
            print("%0.8f\t%d" % (self.values[s], self.pi[s]))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='MDP parser and solver.')
    parser.add_argument('--algorithm',
                        metavar='A',
                        help='MDP algorithm',
                        choices=['lp', 'hpi'])
    parser.add_argument('--mdp',
                        metavar='file_path',
                        help='absolute path to MDP file')
    args = parser.parse_args()

    m = MDP()
    m.read_from_file(args.mdp)

    if args.algorithm == 'lp':
        m.solve_LP()
    elif args.algorithm == 'hpi':
        m.solve_PI()

    m.print()
