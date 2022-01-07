import os
import pandas as pd
import networkx as nx
from clustering_deletion_deleted_edge_greedy.random_edge_greedy import k_clustering_deletion_random_edge_contraction
import time
import matplotlib.pyplot as plt


def read_dataset(directory):
    files = os.listdir(directory)

    for i in range(len(files)):
        file = directory + files[i]
        files[i] = file
    return files


def getGraphs(datasets):
    graphs = []
    for ds in datasets.values():
        # G = nx.read_edgelist(ds, create_using=nx.Graph(), nodetype=str)
        G = read_graph(ds)
        nx.set_edge_attributes(G, 1, 'weight')
        graphs.append(G)
    return graphs


def experiments_dir(datasets_dir, algorithms):
    datasets = read_dataset(datasets_dir)
    experiments(datasets, algorithms)


def experiments(datasets, algorithms):
    dataset_name = list(datasets.keys())
    algorithms_name = list(algorithms.keys())

    graphs = getGraphs(datasets)

    for i in range(len(graphs)):
        n = len(graphs[i].nodes)
        m = len(graphs[i].edges)
        dataset_name[i] = dataset_name[i] + \
            "\n|V|=" + str(n) + "\n|E|=" + str(m)

    df_value = pd.DataFrame(columns=algorithms_name, index=dataset_name)
    df_time = pd.DataFrame(columns=algorithms_name, index=dataset_name)
    df_solution = pd.DataFrame(columns=algorithms_name, index=dataset_name)

    for alg_name, alg in algorithms.items():
        for i in range(len(graphs)):
            print("************************************************************")
            print("exec alg: ", alg_name, " on ds: \n", dataset_name[i] + "\n")
            print("************************************************************")
            start_k = time.time()
            res = k_clustering_deletion_random_edge_contraction(
                graphs[i], 1, choice_method=alg
            )
            end_k = time.time() - start_k
            df_value.at[dataset_name[i], alg_name] = res[0]
            df_time.at[dataset_name[i], alg_name] = end_k
            df_solution.at[dataset_name[i], alg_name] = res[1]

    return df_value, df_time, df_solution


def plot_data_frame(df, title):
    ax = plt.gca()
    g = df.plot(style='.-', ax=ax)
    plt.legend(loc='upper right')
    g.set_title(title, color='black')
    g.legend(bbox_to_anchor=(1.0, 1.0))
    plt.subplots_adjust(right=0.7)
    plt.show()


def read_graph(dataset):
    file = open(dataset, 'r')

    G = nx.Graph()
    for row in file:
        edge_str = row.rstrip('\n')
        edge_pair = edge_str.split(" ")
        G.add_edge(edge_pair[0], edge_pair[1])

    return G
