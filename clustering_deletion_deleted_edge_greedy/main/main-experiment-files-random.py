import networkx as nx
import time
from src.clustering_deletion_edge_contraction_based.util_exp import read_graph
from clustering_deletion_deleted_edge_greedy.random_edge_greedy import clustering_deleteting_random_choice_deleted_edge_greedy,k_clustering_deletion_random_edge_contraction

if __name__ == "__main__":

    datasets = [
        "data/cur_data_exp/FB1",
        # "data/cur_data_exp/FB2",
        # "data/bio/bio-CE-GT",
        # "data/bio/bio-SC-CC",
        # "data/bio/bio-HS-HT.edges",
        # "data/bio/bio-grid-plant.edges",
        # "data/bio/bio-grid-worm.edges"
    ]

    s = ""
    for dataset in datasets:
        G = read_graph(dataset)
        nx.set_edge_attributes(G, 1, 'weight')
        nx.set_edge_attributes(G, -1, 'f')
        nx.set_node_attributes(G, "", "labels")

        for node in G.nodes:
            G.nodes[node]["labels"] = str(node)

        start_k = time.time()
        value = k_clustering_deletion_random_edge_contraction(G,20)
        end_k = time.time() - start_k
        s += "dataset " + str(dataset) + "\n"
        s += "execution time " + str(end_k) + "\n"
        s += "value " + str(value) + "\n"
        s += "*********************************"
    print(s)
