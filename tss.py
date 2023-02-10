import random
from copy import copy
from time import time

from pysat.pb import EncType
from pysat.solvers import Glucose3

import genetic
import tss_sat
import tss_tdg


def exec_with_time(executable):
    time_start = time()
    result = executable()
    time_end = time()
    return result, time_end - time_start


class TSSProblem:

    def __init__(self, dltm, threshold):
        self.dltm = dltm
        self.threshold = threshold

    def nodes_count(self):
        return self.dltm.nodes_count()

    def edges_count(self):
        return self.dltm.edges_count()

    def fit(self, vec):
        n = len(vec)
        if n != self.nodes_count():
            raise ValueError('vector length ({}) != agents number ({})'.format(n, self.nodes_count()))

        start_vec = [1 if a else 0 for a in vec]
        cur_vec = copy(start_vec)
        cur_infl = [0 for _ in range(n)]
        cur_indices = []
        for i in range(n):
            if cur_vec[i]:
                cur_indices.append(i)

        while wt(cur_vec) < self.threshold:
            new_indices = []
            for i in cur_indices:
                agent = self.dltm.ord_to_agent[i]
                for agent_to in self.dltm.graph[agent]:
                    i_to = self.dltm.agent_to_ord[agent_to]
                    cur_infl[i_to] += self.dltm.infl[(agent, agent_to)]
                    if not cur_vec[i_to] and cur_infl[i_to] >= self.dltm.agents[agent_to]:
                        new_indices.append(self.dltm.agent_to_ord[agent_to])
                        cur_vec[i_to] = 1

            if len(new_indices) == 0:
                break
            cur_indices = list(new_indices)

        return wt(start_vec) if wt(cur_vec) >= self.threshold else n + 1

    def solve_abstract(self, solver, seed=None):
        random.seed(seed)
        (solution_vec, metadata), time = exec_with_time(lambda: solver())
        solution = vec_to_agents(self, solution_vec)
        metadata['time'] = time
        return solution, metadata

    def solve_using_1p1(self, stop_criteria, mutation=genetic.non_increasing_default_mutation, seed=None):
        return self.solve_abstract(lambda: genetic.using_1p1(
            [1] * self.nodes_count(), self.fit, mutation, stop_criteria
        ), seed)

    def solve_using_1cl(self, lmbd, stop_criteria, seed=None):
        return self.solve_abstract(lambda: genetic.using_1cl(
            [1] * self.nodes_count(), self.fit, genetic.default_mutation, lmbd, stop_criteria
        ), seed)

    def solve_using_custom_ga(self, l, h, g, stop_criteria, seed=None):
        return self.solve_abstract(lambda: genetic.using_custom_ga(
            [1] * self.nodes_count(), self.fit, genetic.default_mutation, genetic.two_point_crossover, l, h, g, stop_criteria
        ), seed)

    def solve_using_tdg(self, d1, d2):
        solution, solution_time = exec_with_time(lambda: tss_tdg.solve(self, d1, d2))
        return solution, {'time': solution_time}

    def solve_using_tdg_and_then_1p1(self, d1, d2, stop_criteria, seed=None):
        tdg_solution, tdg_solution_time = exec_with_time(lambda: tss_tdg.solve(self, d1, d2))
        solution, metadata = self.solve_abstract(lambda: genetic.using_1p1(
            agents_to_vec(self, tdg_solution), self.fit,
            genetic.non_increasing_default_mutation,
            stop_criteria
        ), seed)
        metadata['time'] = metadata['time'] + tdg_solution_time
        return solution, metadata

    def solve_using_tdg_and_then_doerr_1p1(self, d1, d2, beta, stop_criteria, seed=None):
        env = genetic.init_doerr_env(beta, self.nodes_count() // 2)
        tdg_solution, tdg_solution_time = exec_with_time(lambda: tss_tdg.solve(self, d1, d2))
        solution, metadata = self.solve_abstract(lambda: genetic.using_1p1(
            agents_to_vec(self, tdg_solution), self.fit,
            lambda vec: genetic.non_increasing_doerr_mutation(vec, env),
            stop_criteria
        ), seed)
        metadata['time'] = metadata['time'] + tdg_solution_time
        return solution, metadata

    def solve_using_sat(self, pb_encoding=EncType.seqcounter, sat_solver=lambda cnf: Glucose3(bootstrap_with=cnf)):

        def do_solve():
            n = self.nodes_count()
            if self.fit([0] * n) != n + 1:
                return []

            left = 0
            right = self.threshold
            right_solution = None
            while left + 1 < right:
                mid = (left + right) // 2
                mid_solution = tss_sat.solve_tss(self, mid, pb_encoding, sat_solver)
                if mid_solution:
                    right = mid
                    right_solution = mid_solution
                else:
                    left = mid

            return right_solution if right_solution else tss_sat.solve_tss(self, right, pb_encoding, sat_solver)

        solution, time = exec_with_time(lambda: do_solve())
        return solution, {'time': time}


def wt(vec):
    return sum(vec)


def vec_to_agents(tss, vec):
    agents = []
    for i in range(tss.nodes_count()):
        if vec[i]:
            agents.append(tss.dltm.ord_to_agent[i])
    return agents


def agents_to_vec(tss, agents):
    vec = [0] * tss.nodes_count()
    for agent in agents:
        vec[tss.dltm.agent_to_ord[agent]] = 1
    return vec
