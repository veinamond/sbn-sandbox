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

    print(tss_problem.solve_using_1p1(10000))
    print(tss_problem.solve_using_1cl(10, 1000))
    print(tss_problem.solve_using_1cl(100, 100))
    print(tss_problem.solve_using_1cl(1000, 10))
    print(tss_problem.solve_using_custom_ga(2, 4, 4, 1000))

    # sum_time = 0
    # for _ in range(iterations):
    #     t = timeof(lambda: print(tss_problem.solve_using_1p1(10000)))
    #     sum_time += t
    #     print('Time (1+1): {}'.format(t))
    # print('Average: {}\n'.format(sum_time / iterations))
    #
    # sum_time = 0
    # for _ in range(iterations):
    #     t = timeof(lambda: print(tss_problem.solve_using_1cl(100, 100)))
    #     sum_time += t
    #     print('Time (1,lambda): {}'.format(t))
    # print('Average: {}\n'.format(sum_time / iterations))
