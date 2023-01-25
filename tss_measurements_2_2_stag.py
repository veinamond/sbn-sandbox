import tss_stop_criteria
from tss_measurements_data import tss

if __name__ == '__main__':
    solvers = [
        ('1+1-EA[1000]', lambda problem: problem.solve_using_1p1(tss_stop_criteria.by_stagnation_count(1000))),
        ('1;4-EA[1000]', lambda problem: problem.solve_using_1cl(4, tss_stop_criteria.by_stagnation_count(1000))),
        ('1;20-EA[1000]', lambda problem: problem.solve_using_1cl(20, tss_stop_criteria.by_stagnation_count(1000))),
        ('customGA[2;4;4;1000]', lambda problem: problem.solve_using_custom_ga(2, 4, 4, tss_stop_criteria.by_stagnation_count(1000))),
        ('customGA[4;2;4;1000]', lambda problem: problem.solve_using_custom_ga(4, 2, 4, tss_stop_criteria.by_stagnation_count(1000))),
        ('customGA[4;4;2;1000]', lambda problem: problem.solve_using_custom_ga(4, 4, 2, tss_stop_criteria.by_stagnation_count(1000)))
    ]

    iterations = 10

    with open('measurements/measurements22-stag.csv', 'w') as f:
        f.write('dltm')
        [f.write(',{}'.format(solvers[i][0])) for i in range(len(solvers))]
        f.write('\n')

        for tss_name, tss_instance in tss:
            f.write(tss_name)

            for solver_name, solver in solvers:
                sum = 0
                sum_iter = 0
                sum_time = 0
                for _ in range(iterations):
                    solution, metadata = solver(tss_instance)
                    sum += len(solution)
                    sum_iter += metadata['iterations']
                    sum_time += metadata['time']
                    print('TSS instance {} solved using {}:  iterations={}, time={}, target_set={}'
                          .format(tss_name, solver_name, metadata['iterations'], metadata['time'], solution))
                f.write(',{} {:.3f} {}'.format(sum_iter / iterations, sum_time / iterations, sum / iterations))

            f.write('\n')
