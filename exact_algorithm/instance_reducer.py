import networkx as nx
import numpy as np

from io_func import readGraph_m

def reduce(G: nx.Graph, n_nodes: int, myseed=100):
    np.random.seed(myseed)
    n = G.number_of_nodes()
    n_idx = [i for i in range(0, n)]
    np.random.shuffle(n_idx)
    for rem in range(n_nodes+1, len(n_idx)):
        G.remove_node(rem)


if __name__ == "__main__":
    G = readGraph_m("./bio-CE-GT")
    print("BEFORE >> Nodes: {}, Edges: {}".format(G.number_of_nodes(), G.number_of_edges()))
    reduce(G, 300)
    print("AFTER >> Nodes: {}, Edges: {}".format(G.number_of_nodes(), G.number_of_edges()))
