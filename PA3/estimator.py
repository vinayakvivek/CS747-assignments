import sys
import logging


logging.basicConfig(
    format='[%(levelname)s][%(asctime)s]: %(message)s',
    datefmt="%H:%M:%S",
    level=logging.DEBUG
)


class Experience():

    def __init__(self, s, a, r, s_):
        self.s = s
        self.a = a
        self.r = r
        self.s_ = s_

    def __repr__(self):
        return "(%d, %d, %f, %d)" % (self.s, self.a, self.r, self.s_)


def estimate(S, A, gamma, experiences, eps=1e-8):

    # initialize model variables
    total_transitions = [[[0.0 for s0 in range(S)] for a in range(A)] for s1 in range(S)]
    total_reward = [[[0.0 for s0 in range(S)] for a in range(A)] for s1 in range(S)]
    T_est = [[[0.0 for s0 in range(S)] for a in range(A)] for s1 in range(S)]
    R_est = [[[0.0 for s0 in range(S)] for a in range(A)] for s1 in range(S)]

    pi_est = [[0.0 for a in range(A)] for s in range(S)]
    total_visits = [[0.0 for a in range(A)] for s in range(S)]

    for index, e in enumerate(experiences):

        # logging.debug("index: %d" % (index))

        s = e.s
        a = e.a
        r = e.r
        s_ = e.s_

        total_transitions[s][a][s_] += 1.0
        total_reward[s][a][s_] += r
        total_visits[s][a] += 1.0

        # update T estimates
        for ts in range(S):
            T_est[s][a][ts] = total_transitions[s][a][ts] / sum(total_transitions[s][a])

        # update pi estimates
        for ta in range(A):
            pi_est[s][ta] = total_visits[s][ta] / sum(total_visits[s])

        # update reward estimate
        R_est[s][a][s_] = total_reward[s][a][s_] / total_transitions[s][a][s_]

    # run model evaluation using estimated pi, T and R
    V = [0 for _ in range(S)]

    while True:
        diff = 0
        for s in range(S):
            new_v = 0
            for a in range(A):
                for s_ in range(S):
                    new_v += pi_est[s][a] * T_est[s][a][s_] * (R_est[s][a][s_] + gamma * V[s_])
            diff += (V[s] - new_v) ** 2
            V[s] = new_v

        if diff < eps:
            break

    for v in V:
        print(v)


def main(file_name):

    lines = []
    with open(file_name, 'r') as f:
        lines = f.readlines()

    lines = [x.strip() for x in lines]

    S = int(lines[0])
    A = int(lines[1])
    gamma = float(lines[2])

    lines = [x.split() for x in lines]

    experiences = []
    for i in range(4, len(lines) - 1):
        s = int(lines[i][0])
        a = int(lines[i][1])
        r = float(lines[i][2])
        s_ = int(lines[i+1][0])
        e = Experience(s, a, r, s_)
        experiences.append(e)

    estimate(S, A, gamma, experiences)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Please provide input filename.')
        sys.exit(1)

    file_name = sys.argv[1]
    main(file_name)
