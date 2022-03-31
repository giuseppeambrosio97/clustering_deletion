import random
import time

import networkx as nx
from matplotlib import pyplot as plt

from CCModel1 import CplexCliqueClusteringModel1


def generate_hidden_cliques_instance(num_cliques,
                                     clique_size,
                                     edge_prob,
                                     seed):
    random.seed(seed)
    # crea num_cliques clique con clique_size nodi
    # aggiunge con probabilità edge_prob i restanti archi tra nodi in clique diverse
    C = [set() for i in range(0, num_cliques)]
    node_idx = 0
    for cl in C:
        offset = 0
        while offset<clique_size:
            cl.add(node_idx+offset)
            offset+=1
        node_idx += clique_size

    C_dict = {n: idx for idx, s in enumerate(C) for n in s}

    graph = nx.Graph()
    for cl in C:
        for n1 in cl:
            for n2 in cl:
                if n1 < n2:
                    graph.add_edge(n1, n2)

    for n1 in range(0, graph.number_of_nodes()):
        for n2 in range(0, graph.number_of_nodes()):
            if n1 < n2 and C_dict.get(n1) != C_dict.get(n2):
                if random.random() <= edge_prob:
                    graph.add_edge(n1, n2)

    print("Hidden cliques:", C)
    print("Node-clique dict:", C_dict)
    print("Graph edges:", graph.edges)

    print([i for i in range(0, graph.number_of_nodes())])

    # nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()

    return graph

def write_instance(graph:nx.Graph, filepath:str):
    file = open(filepath,"w")
    firstline = '# {} edges\n'.format(graph.number_of_edges())
    stringedges = ''.join(str(e[0])+" "+str(e[1])+"\n" for e in graph.edges)
    file.write(firstline+stringedges)
    file.close()

def gen_battery_test(folder = "../Instances_Hidden_Cliques_Large"):
    # Parametri size small
    # num_clique = [3, 6, 9, 12, 15]
    # clique_size = [5, 10, 15, 20]
    # edge_prob = [0.1, 0.2, 0.3]
    num_clique = [20, 25, 30, 35, 40]
    clique_size = [10, 15, 20, 25]
    edge_prob = [0.1, 0.2, 0.3]
    for nc in num_clique:
        for cs in clique_size:
            for p in edge_prob:
                file_name = "HC_{}_{}_{}.txt".format(nc, cs, p)
                G = generate_hidden_cliques_instance(num_cliques=nc,
                                                     clique_size=cs,
                                                     edge_prob=p,
                                                     seed=2000)
                write_instance(G, folder+"/"+file_name)


if __name__ == "__main__":
    gen_battery_test()

    # G = generate_hidden_cliques_instance(num_cliques=15,
    #                                      clique_size=20,
    #                                      edge_prob=0.3,
    #                                      seed=2000)

    # write_instance(G, "graph.txt")
    # model = CplexCliqueClusteringModel1(G, verbose=False)

    # start_time = time.time()
    # print("Start time:", start_time)
    # output = model.solve()
    # print(">>>>>> CPLEX clique clustering model TIME:", time.time() - start_time)
    # print(output)

    # if int(output.get("status")) == 101:
    #     color_map = []
    #     for edge in G.edges:
    #         if edge in output.get("edgesSelected") or (edge[1], edge[0]) in output.get("edgesSelected"):
    #             color_map.append('xkcd:coral')
    #         else:
    #             color_map.append('xkcd:grey')

    #     #nx.draw(G, edge_color=color_map, with_labels=True, font_weight='bold')
    #     #plt.show()