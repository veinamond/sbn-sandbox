import tss_stop_criteria
from tss_measurements_data import fb_data_tss

if __name__ == '__main__':
    solvers = [
        ('tdg[1]', lambda problem: problem.solve_using_tdg(1, 1)),
        ('tdg[2]', lambda problem: problem.solve_using_tdg(2, 2)),
        ('tdg[3]', lambda problem: problem.solve_using_tdg(3, 3)),
        ('tdg[5]', lambda problem: problem.solve_using_tdg(5, 5)),
        ('tdg[8]', lambda problem: problem.solve_using_tdg(8, 8)),
        ('1+1[3000]', lambda problem: problem.solve_using_1p1(tss_stop_criteria.by_iteration_count(3000))),
        ('tdg[8]&1+1[3000]', lambda problem: problem.solve_using_tdg_and_then_1p1(8, 8, tss_stop_criteria.by_iteration_count(3000))),
        ('tdg[8]&doerr1+1[1.6;3000]', lambda problem: problem.solve_using_tdg_and_then_doerr_1p1(8, 8, 1.6, tss_stop_criteria.by_iteration_count(3000))),
        ('tdg[8]&doerr1+1[2;3000]', lambda problem: problem.solve_using_tdg_and_then_doerr_1p1(8, 8, 2, tss_stop_criteria.by_iteration_count(3000))),
        ('tdg[8]&doerr1+1[2.5;3000]', lambda problem: problem.solve_using_tdg_and_then_doerr_1p1(8, 8, 2.5, tss_stop_criteria.by_iteration_count(3000)))
    ]

    with open('measurements/measurements31-fb-tdg2.csv', 'w') as f:
        f.write('dltm')
        [f.write(',{}'.format(solvers[i][0])) for i in range(len(solvers))]
        f.write('\n')

        for tss_name, tss in fb_data_tss:
            f.write(tss_name)

            for solver_name, solver in solvers:
                solution, metadata = solver(tss)
                print('TSS instance {} ({} nodes, {} edges) solved using {}:  time={}, ts_size={}, ts={}'
                      .format(tss_name, tss.nodes_count(), tss.edges_count(), solver_name, metadata['time'],
                              len(solution), solution))
                f.write(',{:.3f} {}'.format(metadata['time'], len(solution)))

            f.write('\n')
