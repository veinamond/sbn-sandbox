from time import time

from dltm import DLTM, write_dltm
from tss import TSSProblem


def with_time(executable):
    time_start = time()
    result = executable()
    time_end = time()
    return result, time_end - time_start


if __name__ == '__main__':
    seed = 123

    data = [
        ('ws[30;4;0.2];0.4', DLTM()
         .generate_watts_strogatz_graph(30, 4, 0.2, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.4)),
        ('ws[30;4;0.2];0.7', DLTM()
         .generate_watts_strogatz_graph(30, 4, 0.2, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.7)),
        ('ws[30;10;0.4];0.4', DLTM()
         .generate_watts_strogatz_graph(30, 10, 0.4, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.4)),
        ('ws[30;10;0.4];0.7', DLTM()
         .generate_watts_strogatz_graph(30, 10, 0.4, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.7)),

        ('ws[100;4;0.2];0.4', DLTM()
         .generate_watts_strogatz_graph(100, 4, 0.2, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.4)),
        ('ws[100;4;0.2];0.7', DLTM()
         .generate_watts_strogatz_graph(100, 4, 0.2, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.7)),
        ('ws[100;10;0.4];0.4', DLTM()
         .generate_watts_strogatz_graph(100, 10, 0.4, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.4)),
        ('ws[100;10;0.4];0.7', DLTM()
         .generate_watts_strogatz_graph(100, 10, 0.4, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.7)),

        ('ba[30;3];0.4', DLTM()
         .generate_barabasi_albert_graph(30, 3, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.4)),
        ('ba[30;3];0.7', DLTM()
         .generate_barabasi_albert_graph(30, 3, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.7)),
        ('ba[30;12];0.4', DLTM()
         .generate_barabasi_albert_graph(30, 12, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.4)),
        ('ba[30;12];0.7', DLTM()
         .generate_barabasi_albert_graph(30, 12, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.7)),

        ('ba[100;5];0.4', DLTM()
         .generate_barabasi_albert_graph(100, 5, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.4)),
        ('ba[100;5];0.7', DLTM()
         .generate_barabasi_albert_graph(100, 5, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.7)),
        ('ba[100;30];0.4', DLTM()
         .generate_barabasi_albert_graph(100, 30, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.4)),
        ('ba[100;30];0.7', DLTM()
         .generate_barabasi_albert_graph(100, 30, seed)
         .generate_constant_influences(1)
         .generate_proportional_thresholds(0.7)),
    ]

    # [write_dltm(dltm, 'samples/msr1__{}.txt'.format(name)) for name, dltm in data]

    tss = [(data[i][0], TSSProblem(data[i][1], 100 if i // 4 % 2 else 30)) for i in range(len(data))]

    solvers = [
        ('1+1-EA[2000]', lambda problem: problem.solve_using_1p1(2000)),
        ('1;l-EA[4;500]', lambda problem: problem.solve_using_1cl(4, 500)),
        ('1;l-EA[20;100]', lambda problem: problem.solve_using_1cl(20, 100)),
        ('customGA[2;4;4;200]', lambda problem: problem.solve_using_custom_ga(2, 4, 4, 200)),
        ('customGA[4;2;4;200]', lambda problem: problem.solve_using_custom_ga(4, 2, 4, 200)),
        ('customGA[4;4;2;200]', lambda problem: problem.solve_using_custom_ga(4, 4, 2, 200)),
    ]

    iterations = 10

    with open('measurements/measurements.csv', 'w') as f:
        f.write('dltm')
        [f.write(',{}'.format(solvers[i][0])) for i in range(len(solvers))]
        f.write('\n')

        for tss_name, tss_instance in tss:
            f.write(tss_name)

            for solver_name, solver in solvers:
                sum = 0
                for _ in range(iterations):
                    solution, time_s = with_time(lambda: solver(tss_instance))
                    sum += len(solution)
                    print('TSS instance {} solved using {}:  target_set={}, time={}'.format(tss_name, solver_name,
                                                                                            solution, time_s))
                f.write(',{}'.format(sum / iterations))

            f.write('\n')
