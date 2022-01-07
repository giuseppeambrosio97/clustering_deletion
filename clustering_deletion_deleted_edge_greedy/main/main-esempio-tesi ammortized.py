import networkx as nx
import time
from clustering_deletion_deleted_edge_greedy.edge_greedy_ammortized import clustering_deleteting_choice_deleted_edge_greedy
if __name__ == "__main__":
    edge_list = [('1', '2'), ('2', '3'), ('1', '3'), ('1', '9'), ('1', '7'), ('1', '8'), ('7', '8'),
                 ('7', '9'), ('8', '9'), ('3', '4'), ('3', '5'), ('3', '6'), ('4', '6'), ('4', '5'), ('5', '6')]
    G = nx.Graph(edge_list)
    nx.set_edge_attributes(G, 1, 'weight')
    nx.set_edge_attributes(G, -1, 'f')
    nx.set_node_attributes(G, "", "labels")

    for node in G.nodes:
        G.nodes[node]["labels"] = str(node)

    start_k = time.time()
    value = clustering_deleteting_choice_deleted_edge_greedy(G)
    end_k = time.time() - start_k
    print("execution time ", end_k)
    print("value ", value)
