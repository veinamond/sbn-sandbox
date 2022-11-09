from copy import copy, deepcopy
from math import ceil, sqrt

from pysat.card import *
from pysat.solvers import Glucose3

from sbn import *
from sbn_generator import *


def atleast_equals(lits, eq_lit, first_lit, bound, vpool=IDPool(), encoding=EncType.seqcounter):
    if bound == 0:
        return [[eq_lit]]

    atleast_bd = CardEnc.atleast(lits=lits, bound=bound, vpool=vpool, top_id=None, encoding=encoding)
    for clause in atleast_bd:
        clause.extend([-eq_lit, first_lit])

    atmost_bd = CardEnc.atmost(lits=lits, bound=bound - 1, vpool=vpool, top_id=None, encoding=encoding)
    for clause in atmost_bd:
        clause.append(eq_lit)

    formula = CNF()
    formula.extend(atleast_bd)
    formula.extend(atmost_bd)
    formula.append([eq_lit, -first_lit])
    return formula


def build_cnf_for_problem_1(sbn, instigators, need_to_activate):

    agents = sbn.agents_count()
    if not sbn.is_conforming():
        raise ValueError("Non-conforming SBN given")
    if instigators < 0 or instigators > agents:
        raise ValueError("Invalid instigators number")
    if need_to_activate < 0 or need_to_activate > agents:
        raise ValueError("Invalid agents number to be activated")
    if instigators + need_to_activate > agents:
        raise ValueError("Instigators number + agents to be activated number exceeds total agents count")

    curr_row = list(range(1, agents + 1))         # initial vars in circuit will have IDs from 1 to 'agents'
    vpool = IDPool()
    vpool.occupy(1, agents)

    formula = CNF()
    formula.extend(CardEnc.equals(
        lits=curr_row,
        bound=instigators,
        vpool=vpool,
        top_id=None,
        encoding=EncType.seqcounter)
    )

    idx_to_agent_id = list(sbn.agents.keys())
    agent_id_to_idx = dict((idx_to_agent_id[idx], idx) for idx in range(agents))

    influencers_of = {}
    for i in range(agents):
        agent = idx_to_agent_id[i]
        influencers = sbn.graph.get(agent, [])
        influencers_of[i] = list(agent_id_to_idx[agent_id] for agent_id in influencers)

    bound_of = {}
    for i in range(agents):
        agent = idx_to_agent_id[i]
        bound_of[i] = ceil(len(influencers_of[i]) * sbn.agents[agent].theta)

    for _ in range(need_to_activate):
        new_row = list(vpool.id() for _ in range(agents))
        for i in range(agents):
            influencers_in_curr_row = list(curr_row[j] for j in influencers_of[i])
            formula.extend(atleast_equals(influencers_in_curr_row, new_row[i], i + 1, bound_of[i], vpool))
        curr_row = copy(new_row)

    formula.extend(CardEnc.atleast(
        lits=curr_row,
        bound=instigators + need_to_activate,
        vpool=vpool,
        top_id=None,
        encoding=EncType.seqcounter)
    )

    print(formula.clauses)
    return formula


def extract_solution_of_problem_1(sbn, cnf_solution):
    idx_to_agent_id = list(sbn.agents.keys())

    print(cnf_solution)
    sliced_vars = cnf_solution[:len(sbn.agents)]
    print(sliced_vars)
    true_vars = list(filter(lambda cnf_var: cnf_var > 0, sliced_vars))
    print(true_vars)
    return [idx_to_agent_id[i - 1] for i in true_vars]


if __name__ == '__main__':

    n = 15
    m = 50
    r_sbn = build_conformist_sbn(random_graph__erdos_renyi_m(n, m), 0.8)
    write_sbn(r_sbn, "samples/test_rnd.txt")

    for instigators in range(1, n):
        cnf = build_cnf_for_problem_1(r_sbn, instigators, n - instigators)
        print("{} instigators: {}".format(instigators, cnf.clauses))

        with Glucose3(bootstrap_with=cnf.clauses) as solver:
            if solver.solve():
                cnf_solution = solver.get_model()
                print("               {}\n".format(extract_solution_of_problem_1(r_sbn, cnf_solution)))
                break
            else:
                print("{              no solution.\n")