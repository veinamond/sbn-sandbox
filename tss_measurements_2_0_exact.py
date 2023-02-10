from tss_measurements_data import small_data_tss

if __name__ == '__main__':
    solvers = [
        ('exact-sat[seqcounter;glucose3]', lambda problem: problem.solve_using_sat())
    ]

    with open('measurements/measurements20-exact.csv', 'w') as f:
        f.write('dltm')
        [f.write(',{}'.format(solvers[i][0])) for i in range(len(solvers))]
        f.write('\n')

        for tss_name, tss_instance in small_data_tss:
            if tss_name.__contains__('[100'):
                continue
            f.write(tss_name)

            for solver_name, solver in solvers:
                solution, metadata = solver(tss_instance)
                print('TSS instance {} solved using {}:  time={}, target_set={}'
                      .format(tss_name, solver_name, metadata['time'], solution))
                f.write(',{:.3f} {}'.format(metadata['time'], len(solution)))

            f.write('\n')
