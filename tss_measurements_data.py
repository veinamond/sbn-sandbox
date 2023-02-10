from math import ceil

from dltm import DLTM
from tss import TSSProblem

seed = 123

small_data = [
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

fb_data = [
    # ('fb_1_0.2', DLTM()
    #  .read_graph_as_edge_list('samples/facebook_combined.txt', False)
    #  .generate_constant_influences(1)
    #  .generate_proportional_thresholds(0.2)),
    # ('fb_1_0.5', DLTM()
    #  .read_graph_as_edge_list('samples/facebook_combined.txt', False)
    #  .generate_constant_influences(1)
    #  .generate_proportional_thresholds(0.5)),
    ('fb_1_0.8', DLTM()
     .read_graph_as_edge_list('samples/facebook_combined.txt', False)
     .generate_constant_influences(1)
     .generate_proportional_thresholds(0.8)),
    ('fb_[1;5]_0.2', DLTM()
     .read_graph_as_edge_list('samples/facebook_combined.txt', False)
     .generate_range_influences(1, 5, seed=123)
     .generate_proportional_thresholds(0.2)),
    ('fb_[1;5]_0.5', DLTM()
     .read_graph_as_edge_list('samples/facebook_combined.txt', False)
     .generate_range_influences(1, 5, seed=123)
     .generate_proportional_thresholds(0.5)),
    ('fb_[1;5]_0.8', DLTM()
     .read_graph_as_edge_list('samples/facebook_combined.txt', False)
     .generate_range_influences(1, 5, seed=123)
     .generate_proportional_thresholds(0.8)),
]

small_data_tss = [(small_data[i][0], TSSProblem(small_data[i][1], small_data[i][1].nodes_count())) for i in range(len(small_data))]

fb_data_tss = [(fb_data[i][0], TSSProblem(fb_data[i][1], ceil(fb_data[i][1].nodes_count() * 0.75))) for i in range(len(fb_data))]
