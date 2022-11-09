import random

from sbn import *


def add_edge(graph, e_from, e_to):
    if not (e_from in graph):
        graph[e_from] = set()
    graph[e_from].add(e_to)


def invert_graph(graph):
    inv_graph = {}
    for e_from, es_to in graph.items():
        for e_to in es_to:
            add_edge(inv_graph, e_to, e_from)
    return inv_graph


def random_sample(n, k):
    s = list(range(0, n))
    r = list(range(0, k))
    for i in range(k, n):
        j = random.randint(0, i)
        if j < k:
            r[j] = s[i]
    return r


def random_graph__erdos_renyi_p(n, p, seed=None):
    random.seed(seed)

    graph = {i: set() for i in range(1, n + 1)}
    for e_from in range(1, n + 1):
        for e_to in range(1, n + 1):
            if e_from == e_to:
                continue
            if random.random() < p:
                add_edge(graph, e_from, e_to)

    return graph


def random_graph__erdos_renyi_m(n, m, seed=None):
    random.seed(seed)

    edges_count = n * (n - 1)
    graph = {i: set() for i in range(1, n + 1)}
    edge_ids = random_sample(edges_count, m)
    for edge_id in edge_ids:
        e_from = edge_id // (n - 1)
        e_to = edge_id % (n - 1)
        if e_to == e_from:
            e_to += 1
        add_edge(graph, e_from + 1, e_to + 1)

    return graph


def build_conformist_sbn(graph, theta):
    sbn = SBN()
    sbn.graph = graph
    sbn.inv_graph = invert_graph(graph)

    agent_ids = sbn.graph.keys() | (sbn.inv_graph.keys() | set())
    [sbn.put_agent(agent_id, Agent(AgentType.conformist, theta)) for agent_id in agent_ids]

    return sbn
