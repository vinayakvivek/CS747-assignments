import argparse


def encode_gambler(ph, N=100):
    S = N + 1  # 0(T, lose), 1, .., 99, 100(T, win)
    A = N  # 0..99

    R = [[[0.0 for s in range(S)] for a in range(A)] for s in range(S)]
    T = [[[0.0 for s in range(S)] for a in range(A)] for s in range(S)]

    for s in range(1, S-1):
        for a in range(A):
            if a > min(s, N - s):
                break
            if s + a == N:
                R[s][a][N] = 1.0

    for s in range(1, S-1):
        for a in range(A):
            if a > min(s, N - s):
                break
            T[s][a][s + a] = ph
            T[s][a][s - a] = (1 - ph)

    print(S)
    print(A)

    for s in range(0, S):
        for a in range(0, A):
            for sPrime in range(0, S):
                print(str(R[s][a][sPrime]) + "\t", end='')
            print()

    for s in range(0, S):
        for a in range(0, A):
            for sPrime in range(0, S):
                print(str(T[s][a][sPrime]) + "\t", end='')
            print()

    print(1.0)
    print('episodic')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gambler problem.')
    parser.add_argument('-N',
                        '--goal',
                        metavar='n',
                        type=int,
                        help='goal of gambler')
    parser.add_argument('-p',
                        '--prob',
                        metavar='P',
                        type=float,
                        help='coin head probability')
    args = parser.parse_args()
    encode_gambler(args.prob, args.goal)