import csv
import os

import networkx as nx

from deepstruct.node_map_strategies import AdjustableNodeMap
from deepstruct.traverse_strategies import FXTraversal
from deepstruct.flexible_transform import GraphTransform
import platform
import psutil
import time


def get_model_graph_stats(model, input, rounds: int, model_name, file_name, low_level_module_maps=None):
    if low_level_module_maps is None:
        low_level_module_maps = {}
    entries = []
    sys_info = get_system_info()
    source = 'Laptop'
    nodemap = AdjustableNodeMap(low_level_module_maps)
    graph_transformer = GraphTransform(input, traversal_strategy=FXTraversal(), node_map_strategy=nodemap)
    graphs = []

    for i in range(rounds):
        start_time = time.perf_counter()
        graph_transformer.transform(model)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        entries.append([source, model_name, elapsed_time])
        graphs.append(graph_transformer.get_graph())

    #for g in graphs:
    #    assert nx.is_isomorphic(graphs[0], g)

    directory_path = 'graph_stats'
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_name_with_suffix = file_name + '.csv'
    file_path = os.path.join(directory_path, file_name_with_suffix)
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Source', 'Model', 'Elapsed Time'])
        csvwriter.writerows(entries)
    return graphs


def get_system_info():
    info = {}
    info['platform'] = platform.system()
    info['platform-release'] = platform.release()
    info['platform-version'] = platform.version()
    info['architecture'] = platform.machine()
    # info['hostname'] = platform.node()
    # info['ip-address'] = socket.gethostbyname(socket.gethostname())
    # info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    info['processor'] = platform.processor()
    info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
    return info
