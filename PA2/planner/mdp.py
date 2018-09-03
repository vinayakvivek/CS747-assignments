import re
from copy import deepcopy
from pulp import LpProblem, LpMinimize, LpVariable,\
    LpStatus, value, LpStatusOptimal
import numpy as np


def clean_line(line):
    line = re.sub(' +', '', line)
    line = line.split('\t')
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

    def solve_lp(self):

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

    def print(self):
        for s in range(self.S):
            print("%0.8f\t%d" % (self.values[s], self.pi[s]))


m = MDP()
file_path = '/Users/vinayakvivek/pro/acads/SEM7/cs747/PA2/data/continuing/MDP10.txt'
m.read_from_file(file_path)
m.solve_lp()
m.print()
