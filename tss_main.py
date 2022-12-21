from dltm import DLTM
from time import time
from tss import TSSProblem


def timeof(executable):
    time_start = time()
    executable()
    time_end = time()
    return time_end - time_start


if __name__ == '__main__':
    dltm = DLTM()
    dltm.generate_gnm_random_graph(100, 1500, seed=12345)
    dltm.generate_range_influences(1, 4, seed=12345)
    dltm.generate_proportional_thresholds(0.5)

    tss_problem = TSSProblem(dltm, 80)

    iterations = 10

    sum_time = 0
    for _ in range(iterations):
        t = timeof(lambda: print(tss_problem.solve_using_1p1_naive(10000)))
        sum_time += t
        print('Time (1+1, naive fit): {}'.format(t))
    print('Average: {}\n'.format(sum_time / iterations))

    sum_time = 0
    for _ in range(iterations):
        t = timeof(lambda: print(tss_problem.solve_using_1p1(10000)))
        sum_time += t
        print('Time (1+1, optimal fit): {}'.format(t))
    print('Average: {}\n'.format(sum_time / iterations))
