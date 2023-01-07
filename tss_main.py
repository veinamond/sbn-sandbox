import tss_stop_criteria
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

    print(tss_problem.solve_using_1p1(tss_stop_criteria.by_iteration_count(10000)))
    print(tss_problem.solve_using_1cl(10, tss_stop_criteria.by_iteration_count(1000)))
    print(tss_problem.solve_using_1cl(100, tss_stop_criteria.by_iteration_count(100)))
    print(tss_problem.solve_using_1cl(1000, tss_stop_criteria.by_iteration_count(10)))
    print(tss_problem.solve_using_custom_ga(2, 4, 4, tss_stop_criteria.by_iteration_count(1000)))
