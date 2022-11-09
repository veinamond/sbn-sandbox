class AgentType:

    conformist = 0
    anticonformist = 1


agent_type_id_to_str = {
    AgentType.conformist: 'conf',
    AgentType.anticonformist: 'anticonf'
}

agent_type_str_to_id = {v: k for k, v in agent_type_id_to_str.items()}


class Agent:

    def __init__(self, agent_type, theta):
        if theta < 0 or theta > 1:
            raise ValueError('Theta argument must be in [0;1] range')
        if agent_type is None:
            raise ValueError('Invalid agent type')
        self.agent_type = agent_type
        self.theta = theta

    def __str__(self):
        return '{} theta={}'.format(agent_type_id_to_str[self.agent_type], self.theta)


class SBN:

    def __init__(self):
        self.agents = {}
        self.graph = {}
        self.inv_graph = {}

    def agents_count(self):
        return len(self.agents)

    def put_agent(self, agent_id, agent):
        self.agents[agent_id] = agent

    def put_agents(self, agent_pairs):
        for a_id, a in agent_pairs:
            self.put_agent(a_id, a)

    def add_edge(self, from_id, to_id):
        # if not (from_id in self.agents):
        #     raise ValueError("Unknown agent: {}".format(from_id))
        # if not (to_id in self.agents):
        #     raise ValueError("Unknown agent: {}".format(to_id))

        if not (from_id in self.graph):
            self.graph[from_id] = []
        self.graph[from_id].append(to_id)

        if not (to_id in self.inv_graph):
            self.inv_graph[to_id] = []
        self.inv_graph[to_id].append(from_id)

    def add_edges(self, from_to_pairs):
        for from_id, to_id in from_to_pairs:
            self.add_edge(from_id, to_id)

    def is_conforming(self):
        return all(agent.agent_type == AgentType.conformist for agent in self.agents.values())


def read_sbn(path):
    with open(path) as f:
        sbn = SBN()

        for line in f.readlines():
            sep_pos = line.rfind("#")
            line_content = line if sep_pos == -1 else line[:sep_pos]
            line_args = line_content.split()

            if len(line_args) == 0:
                continue
            if len(line_args) == 1:
                raise ValueError("Too few arguments, expected either agent declaration or edge(s), got {}".format(line_content))
            else:
                if line_args[1] == '=':
                    if len(line_args) < 4:
                        raise ValueError("Too few arguments at agent declaration. Expected '<agent_id> = <conf|anticonf> <theta>', got {}".format(line_content))
                    sbn.put_agent(line_args[0], Agent(agent_type_str_to_id[line_args[2]], float(line_args[3])))
                else:
                    if line_args[1] == '<-':
                        [sbn.add_edge(line_args[0], to) for to in line_args[2:]]
                    else:
                        raise ValueError("Expected either agent declaration ('a = ...') or edge(s) ('a <- ...'), got {}".format(line_content))

        return sbn


def write_sbn(sbn, path):
    file = open(path, "w")

    for agent_id in sbn.agents.keys():
        agent = sbn.agents[agent_id]
        file.write("{} = {} {}\n".format(agent_id, agent_type_id_to_str[agent.agent_type], agent.theta))
    file.write("\n")

    for v in sbn.graph.keys():
        file.write("{} <-".format(v))
        for u in sbn.graph[v]:
            file.write(" {}".format(u))
        file.write("\n")
