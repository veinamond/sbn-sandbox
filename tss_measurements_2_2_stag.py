import tss_stop_criteria
from tss_measurements_data import small_data_tss

if __name__ == '__main__':
    solvers = [
        ('1+1-EA[1000]', lambda problem: problem.solve_using_1p1(tss_stop_criteria.by_stagnation_count(1000))),
        ('1;4-EA[1000]', lambda problem: problem.solve_using_1cl(4, tss_stop_criteria.by_stagnation_count(1000))),
        ('1;20-EA[1000]', lambda problem: problem.solve_using_1cl(20, tss_stop_criteria.by_stagnation_count(1000))),
        ('customGA[2;4;4;1000]', lambda problem: problem.solve_using_custom_ga(2, 4, 4, tss_stop_criteria.by_stagnation_count(1000))),
        ('customGA[4;2;4;1000]', lambda problem: problem.solve_using_custom_ga(4, 2, 4, tss_stop_criteria.by_stagnation_count(1000))),
        ('customGA[4;4;2;1000]', lambda problem: problem.solve_using_custom_ga(4, 4, 2, tss_stop_criteria.by_stagnation_count(1000))),
        ('tdg[1]', lambda problem: problem.solve_using_tdg(1, 1)),
        ('tdg[2]', lambda problem: problem.solve_using_tdg(2, 2)),
        ('tdg[3]', lambda problem: problem.solve_using_tdg(3, 3)),
        ('tdg[5]', lambda problem: problem.solve_using_tdg(5, 5))
    ]

    with open('measurements/measurements22-stag.csv', 'w') as f:
        f.write('dltm')
        [f.write(',{}'.format(solvers[i][0])) for i in range(len(solvers))]
        f.write('\n')

        for tss_name, tss_instance in small_data_tss:
            f.write(tss_name)

            for solver_name, solver in solvers:
                iterations = 1 if solver_name.startswith('tdg') else 10
                sum = 0
                sum_iters = 0
                sum_time = 0
                for _ in range(iterations):
                    solution, metadata = solver(tss_instance)
                    iters = metadata['iterations'] if 'iterations' in metadata else None

                    sum += len(solution)
                    sum_iters = sum_iters + iters if iters else None
                    sum_time += metadata['time']

                    print('TSS instance {} solved using {}:  iterations={}, time={}, target_set={}'
                          .format(tss_name, solver_name, iters, metadata['time'], solution))
                mid_iters = sum_iters / iterations if sum_iters else None
                f.write(',{} {:.3f} {}'.format(mid_iters, sum_time / iterations, sum / iterations))

            f.write('\n')
