import math
import numpy as np
import random
from scipy.special import softmax
import copy


class RangedHeap:
    def __init__(self, G):
        self.size = len(G.edges)
        self.fs = [{} for _ in range(len(G.nodes))]
        self.bool_fs = []

        for e in G.edges:
            val = f(G, e)
            G[e[0]][e[1]]['f'] = val
            e = self.get_e(e[0], e[1])
            self.fs[val][e] = e

        for id, id_map in enumerate(self.fs):
            if len(id_map) != 0:
                self.bool_fs.append(id)

    def getMin(self, G):
        if self.size >= 1:
            edge_to_pick = self.getMinTwins(G)
            # out = self.fs[self.bool_fs[0]].popitem()[1]
            self.size -= 1
            if len(self.fs[self.bool_fs[0]]) == 0:
                del self.bool_fs[0]
            return edge_to_pick
        else:
            print("RangedHeap is empty")

    def getRand(self, G):
        if self.bool_fs[0] != 0:
            n = np.sum(self.bool_fs)
            prob_list = [n / e for e in self.bool_fs]
            norm = np.sum(prob_list)
            prob_list = [e/norm for e in prob_list]
            f_to_pick = np.random.choice(self.bool_fs, size=1, p=prob_list)[0]
            edge_to_pick = random.choice(list(self.fs[f_to_pick].values()))
            del self.fs[f_to_pick][edge_to_pick]
            self.size -= 1
            if len(self.fs[f_to_pick]) == 0:
                self.binary_search_delete(f_to_pick)
        else:
            edge_to_pick = self.getMin(G)

        return edge_to_pick

    def getSoftMaxRand(self, G):
        if self.bool_fs[0] != 0:
            n = np.sum(self.bool_fs)
            prob_list = [n / e for e in self.bool_fs]
            prob_list = softmax(prob_list)
            # print(prob_list)
            f_to_pick = np.random.choice(self.bool_fs, size=1, p=prob_list)[0]
            edge_to_pick = random.choice(list(self.fs[f_to_pick].values()))
            del self.fs[f_to_pick][edge_to_pick]
            self.size -= 1
            if len(self.fs[f_to_pick]) == 0:
                self.binary_search_delete(f_to_pick)
        else:
            edge_to_pick = self.getMin(G)

        return edge_to_pick

    def getMinTwins(self, G):
        weight_max = -math.inf
        edge_to_pick = None
        for _, e in self.fs[self.bool_fs[0]].items():
            w = G[e[0]][e[1]]['weight']
            if weight_max < w:
                weight_max = w
                edge_to_pick = e
        del self.fs[self.bool_fs[0]][edge_to_pick]
        return edge_to_pick

    def delete_e(self, e0, e1, f):
        e = self.get_e(e0, e1)
        del self.fs[f][e]
        self.size -= 1

        if len(self.fs[f]) == 0:
            self.binary_search_delete(f)

    def add(self, e0, e1, f):
        e = self.get_e(e0, e1)
        if len(self.fs[f]) == 0:
            self.binary_search_add(f)
        self.fs[f][e] = e
        self.size += 1

    def adjust(self, e0, e1, old_f, new_f):
        e = self.get_e(e0, e1)
        self.delete_e(e[0], e[1], old_f)
        self.add(e[0], e[1], new_f)

    def binary_search_delete(self, x):
        l = 0
        r = len(self.bool_fs)-1

        while l <= r:
            c = (l + r) // 2
            if self.bool_fs[c] == x:
                break
            elif self.bool_fs[c] < x:
                l = c + 1
            else:
                r = c - 1
        del self.bool_fs[c]

    def binary_search_add(self, x):
        if len(self.bool_fs) > 0:
            if x < self.bool_fs[0]:
                self.bool_fs.insert(0, x)
            elif x > self.bool_fs[-1]:
                self.bool_fs.append(x)
            else:
                l = 0
                r = len(self.bool_fs)-1

                while l <= r:
                    c = (l + r) // 2
                    if self.bool_fs[c] < x:
                        if x < self.bool_fs[c+1]:
                            break
                        else:
                            l = c + 1
                    else:
                        r = c - 1
                self.bool_fs.insert(c+1, x)
        else:
            self.bool_fs.append(x)

    def get_e(self, e0, e1):
        return (e0, e1) if int(e0) < int(e1) else (e1, e0)

    def print_fs(self):
        for id, id_map in enumerate(self.fs):
            values = ""
            for key, value in id_map.items():
                values += " " + str(value)
            s = "[" + str(id) + "]->" + values + "\n"
            print(s)

    def prinf_bool_fs(self):
        print(self.bool_fs)

    def __len__(self):
        return self.size


def f(G, e):
    vicini0 = set(G.neighbors(e[0]))
    vicini0.remove(e[1])
    vicini1 = set(G.neighbors(e[1]))
    vicini1.remove(e[0])

    A = vicini0 - vicini1  # vicini di e[0] e non di e[1]
    C = vicini1 - vicini0

    value = 0

    for node in A:  # removed
        value += G[e[0]][node]['weight']

    for node in C:  # removed
        value += G[e[1]][node]['weight']

    return value


def preprocess(G):
    rangedHeap = RangedHeap(G)
    value = 0
    while True:
        e = rangedHeap.getMin(G)
        if(G[e[0]][e[1]]['f'] > 0):
            break
        edge_contraction(G, e, rangedHeap)
    return value


def edge_contraction(G, e, rangedHeap):
    vicini0 = set(G.neighbors(e[0]))
    vicini0.remove(e[1])
    vicini1 = set(G.neighbors(e[1]))
    vicini1.remove(e[0])

    Ne0_e1 = vicini0 - vicini1  # vicini di e[0] e non di e[1]
    Ne0e1 = vicini0 & vicini1  # vicini di e[0] e di e[1]
    Ne1_e0 = vicini1 - vicini0  # vicini di e[1] e non di e[0]

    for node in Ne0_e1:  # removed
        rangedHeap.delete_e(e[0], node, G[e[0]][node]['f'])
        G.remove_edge(e[0], node)

    for node in Ne1_e0:  # removed
        rangedHeap.delete_e(e[1], node, G[e[1]][node]['f'])

    for node in Ne0e1:
        G[e[0]][node]['weight'] += G[e[1]][node]['weight']
        rangedHeap.delete_e(e[0], node, G[e[0]][node]['f'])
        rangedHeap.delete_e(e[1], node, G[e[1]][node]['f'])

    G.nodes[e[0]]["labels"] += "-" + G.nodes[e[1]]["labels"]
    G.remove_node(e[1])

    for node in Ne0e1:
        new_f = f(G, (e[0], node))
        G[e[0]][node]['f'] = new_f
        rangedHeap.add(e[0], node, new_f)

    toAdjust = G.edges(list(Ne0_e1)+list(Ne0e1)+list(Ne1_e0))
    for edge in toAdjust:
        if edge[0] != e[0] and edge[1] != e[0]:
            new_f = f(G, edge)
            old_f = G[edge[0]][edge[1]]['f']
            if new_f != old_f:
                G[edge[0]][edge[1]]['f'] = new_f
                rangedHeap.adjust(edge[0], edge[1], old_f, new_f)


def clustering_deleteting_choice_deleted_edge_greedy(G, rangedHeap):
    value = 0
    while len(rangedHeap) != 0:
        e = rangedHeap.getMin(G)
        value += G[e[0]][e[1]]['f']
        edge_contraction(G, e, rangedHeap)
    return value


def clustering_deleteting_choice_deleted_edge_greedy(G, deep_k, rangedHeap):
    value = 0
    i = 0
    while i < deep_k or len(rangedHeap) != 0:
        e = rangedHeap.getMin(G)
        value += G[e[0]][e[1]]['f']
        edge_contraction(G, e, rangedHeap)
        i += 1
    return value


def clustering_deleteting_random_choice_deleted_edge_greedy(G, rangedHeap):
    value = 0
    while len(rangedHeap) != 0:
        e = rangedHeap.getSoftMaxRand(G)
        value += G[e[0]][e[1]]['f']
        edge_contraction(G, e, rangedHeap)
    return value


def clustering_deleteting_random_choice_deleted_edge_greedy(G, deep_k, rangedHeap):
    value = 0
    i = 0
    while i < deep_k or len(rangedHeap) != 0:
        e = rangedHeap.getSoftMaxRand(G)
        value += G[e[0]][e[1]]['f']
        edge_contraction(G, e, rangedHeap)
        i += 1
    return value


def fork_clustering_deleteting_random_choice_deleted_edge_greedy(G, fork_k, deep_k, rangedHeap_G):

    H = G.copy()
    rangedHeap_H = copy.deepcopy(rangedHeap_G)
    min_val = clustering_deleteting_choice_deleted_edge_greedy(
        H, deep_k, rangedHeap_H)
    rangedHeap_min = rangedHeap_H
    G_min = H


    for _ in range(fork_k):
        H = G.copy()
        rangedHeap_H = copy.deepcopy(rangedHeap_G)
        val = clustering_deleteting_random_choice_deleted_edge_greedy(
            H, deep_k, rangedHeap_H)
        if val < min_val:
            min_val = val
            G_min = H
            rangedHeap_min = rangedHeap_H

    return G_min, rangedHeap_min, min_val


def alg(G, fork_k, deep_k):
    rangedHeap = RangedHeap(G)
    sol = 0
    while len(rangedHeap) != 0:
        val = 0
        if rangedHeap.bool_fs[0] > 0:
            G, rangedHeap, val = fork_clustering_deleteting_random_choice_deleted_edge_greedy(
                G, fork_k, deep_k, rangedHeap)
        else:
            e = rangedHeap.getMin(G)
            val = G[e[0]][e[1]]['f']
            edge_contraction(G, e, rangedHeap)
        sol += val
    return sol


def k_clustering_deletion_random_edge_contraction(G, k):
    """
    INPUT:
        G: networkx graph
        k: number of times that clustering_deletion_random_edge_contraction must be executed
    OUTPUT:
        min_val: value of the solution with the minimum value among the k discovered
        min_partition: partition of the set of vertices identified by the solution with value min_value
    """

    min_val = math.inf

    import pandas as pd

    df = pd.DataFrame(np.zeros((k, 2)), columns=["exec", "v_min"])

    rangedHeap_G = RangedHeap(G)

    for i in range(k):
        H = G.copy()
        rangedHeap_H = copy.deepcopy(rangedHeap_G)
        val = clustering_deleteting_random_choice_deleted_edge_greedy(
            H, rangedHeap_H)
        df.at[i, 'exec'] = val
        if val < min_val:
            min_val = val
        df.at[i, 'v_min'] = min_val

    import seaborn as sns
    print(df)
    sns.lineplot(data=df)

    return min_val
