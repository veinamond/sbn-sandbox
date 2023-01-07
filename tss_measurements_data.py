from dltm import DLTM
from tss import TSSProblem

seed = 123

data = [
    ('ws[30;4;0.2];0.4', DLTM()
     .generate_watts_strogatz_graph(30, 4, 0.2, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.4)),
    ('ws[30;4;0.2];0.7', DLTM()
     .generate_watts_strogatz_graph(30, 4, 0.2, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.7)),
    ('ws[30;10;0.4];0.4', DLTM()
     .generate_watts_strogatz_graph(30, 10, 0.4, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.4)),
    ('ws[30;10;0.4];0.7', DLTM()
     .generate_watts_strogatz_graph(30, 10, 0.4, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.7)),

    ('ws[100;4;0.2];0.4', DLTM()
     .generate_watts_strogatz_graph(100, 4, 0.2, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.4)),
    ('ws[100;4;0.2];0.7', DLTM()
     .generate_watts_strogatz_graph(100, 4, 0.2, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.7)),
    ('ws[100;10;0.4];0.4', DLTM()
     .generate_watts_strogatz_graph(100, 10, 0.4, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.4)),
    ('ws[100;10;0.4];0.7', DLTM()
     .generate_watts_strogatz_graph(100, 10, 0.4, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.7)),

    ('ba[30;3];0.4', DLTM()
     .generate_barabasi_albert_graph(30, 3, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.4)),
    ('ba[30;3];0.7', DLTM()
     .generate_barabasi_albert_graph(30, 3, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.7)),
    ('ba[30;12];0.4', DLTM()
     .generate_barabasi_albert_graph(30, 12, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.4)),
    ('ba[30;12];0.7', DLTM()
     .generate_barabasi_albert_graph(30, 12, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.7)),

    ('ba[100;5];0.4', DLTM()
     .generate_barabasi_albert_graph(100, 5, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.4)),
    ('ba[100;5];0.7', DLTM()
     .generate_barabasi_albert_graph(100, 5, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.7)),
    ('ba[100;30];0.4', DLTM()
     .generate_barabasi_albert_graph(100, 30, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.4)),
    ('ba[100;30];0.7', DLTM()
     .generate_barabasi_albert_graph(100, 30, seed)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.7)),
]

tss = [(data[i][0], TSSProblem(data[i][1], 100 if i // 4 % 2 else 30)) for i in range(len(data))]
