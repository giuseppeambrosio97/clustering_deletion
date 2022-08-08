import os
from typing import Any, List, Tuple
import networkx as nx


def read_graph(dataset: str) -> nx.Graph:
    file = open(dataset, 'r')

    G = nx.Graph()
    for row in file:
        if row[0] != '#':
            edge_str = row.rstrip('\n')
            edge_pair = edge_str.split(" ")
            if len(edge_pair) >= 2:
                G.add_edge(int(edge_pair[0]), int(edge_pair[1]))

    return G


def read_dataset(directory: str) -> List[str]:
    files = os.listdir(directory)

    for i in range(len(files)):
        file = directory + files[i]
        files[i] = file
    return files


def get_e(e0: Any, e1: Any) -> Tuple[Any, Any]:
    return (e0, e1) if e0 < e1 else (e1, e0)

