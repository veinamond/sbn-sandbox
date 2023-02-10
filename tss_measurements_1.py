import tss_stop_criteria
from tss_measurements_data import small_data_tss


if __name__ == '__main__':
    solvers = [
        ('1+1-EA[2000]', lambda problem: problem.solve_using_1p1(tss_stop_criteria.by_iteration_count(2000))),
        ('1;4-EA[500]', lambda problem: problem.solve_using_1cl(4, tss_stop_criteria.by_iteration_count(500))),
        ('1;20-EA[100]', lambda problem: problem.solve_using_1cl(20, tss_stop_criteria.by_iteration_count(100))),
        ('customGA[2;4;4;200]', lambda problem: problem.solve_using_custom_ga(2, 4, 4, tss_stop_criteria.by_iteration_count(200))),
        ('customGA[4;2;4;200]', lambda problem: problem.solve_using_custom_ga(4, 2, 4, tss_stop_criteria.by_iteration_count(200))),
        ('customGA[4;4;2;200]', lambda problem: problem.solve_using_custom_ga(4, 4, 2, tss_stop_criteria.by_iteration_count(200))),
        ('tdg[1]', lambda problem: problem.solve_using_tdg(1, 1)),
        ('tdg[2]', lambda problem: problem.solve_using_tdg(2, 2)),
        ('tdg[3]', lambda problem: problem.solve_using_tdg(3, 3)),
        ('tdg[5]', lambda problem: problem.solve_using_tdg(5, 5))
    ]

    with open('measurements/measurements1.csv', 'w') as f:
        f.write('dltm')
        [f.write(',{}'.format(solvers[i][0])) for i in range(len(solvers))]
        f.write('\n')

        for tss_name, tss_instance in small_data_tss:
            f.write(tss_name)

            for solver_name, solver in solvers:
                iterations = 1 if solver_name.startswith('tdg') else 10
                sum = 0
                for _ in range(iterations):
                    solution, metadata = solver(tss_instance)
                    sum += len(solution)
                    print('TSS instance {} solved using {}:  target_set={}, time={}'
                          .format(tss_name, solver_name, solution, metadata['time']))
                f.write(',{}'.format(sum / iterations))

            f.write('\n')
