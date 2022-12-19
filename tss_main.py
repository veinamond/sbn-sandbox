from dltm import write_dltm, DLTM
from tss import TSSProblem

if __name__ == '__main__':
    dltm = DLTM()
    dltm.generate_barabasi_albert_graph(20, 4, seed=12345)
    dltm.generate_range_influences(1, 4, seed=12345)
    dltm.generate_proportional_thresholds(0.3)
    write_dltm(dltm, 'samples/dltm_test_rnd.txt')

    tss_problem = TSSProblem(dltm, 15)

    print(tss_problem.solve_using_1p1(10000))
    print(tss_problem.solve_using_1cl(100, 100))
