import sys


class Experience():

    def __init__(self, s, a, r, s_):
        self.s = s
        self.a = a
        self.r = r
        self.s_ = s_

    def __repr__(self):
        return "(%d, %d, %f, %d)" % (self.s, self.a, self.r, self.s_)


def TD_0(S, A, gamma, experiences, alpha=0.01):

    V = [0 for x in range(S)]

    for index, e in enumerate(experiences):
        diff = e.r + gamma * V[e.s_] - V[e.s]
        V[e.s] += alpha * diff

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

    TD_0(S, A, gamma, experiences, alpha=0.01)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Please provide input filename.')
        sys.exit(1)

    file_name = sys.argv[1]
    main(file_name)