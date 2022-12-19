from copy import copy

import evol


class TSSProblem:

    def __init__(self, dltm, threshold):
        self.dltm = dltm
        self.threshold = threshold

    def fit(self, vec):
        n = len(vec)
        if n != len(self.dltm.ord_to_agent):
            raise ValueError('vector length ({}) != agents number ({})'.format(n, len(self.dltm.ord_to_agent)))

        start_vec = [1 if a else 0 for a in vec]
        cur_vec = copy(start_vec)
        while wt(cur_vec) < self.threshold:
            cur_infl = [0 for _ in range(n)]
            for i in range(n):
                if cur_vec[i]:
                    agent = self.dltm.ord_to_agent[i]
                    for agent_to in self.dltm.graph[agent]:
                        cur_infl[self.dltm.agent_to_ord[agent_to]] += self.dltm.infl[(agent, agent_to)]

            new_vec = []
            for i in range(n):
                new_vec.append(1 if start_vec[i] or (cur_infl[i] >= self.dltm.agents[self.dltm.ord_to_agent[i]]) else 0)

            if new_vec == cur_vec:
                break
            cur_vec = new_vec

        return wt(start_vec) if wt(cur_vec) >= self.threshold else n + 1

    def solve_abstract(self, solver, seed=None):
        solution_vec = solver(seed)
        solution = []
        for i in range(len(solution_vec)):
            if solution_vec[i]:
                solution.append(self.dltm.ord_to_agent[i])
        return solution

    def solve_using_1p1(self, iterations, seed=None):
        return self.solve_abstract(lambda sd: evol.using_1p1(
            [0 for _ in range(len(self.dltm.agents))], self.fit, iterations, sd
        ), seed)

    def solve_using_1cl(self, lmbd, iterations, seed=None):
        return self.solve_abstract(lambda sd: evol.using_1cl(
            [0 for _ in range(len(self.dltm.agents))], self.fit, lmbd, iterations, sd
        ), seed)


def wt(vec):
    return sum(vec)
