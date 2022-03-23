import math
from typing import Set, Tuple
import networkx as nx
from deleted_edge_greedy.util_exp import get_e


class EdgeBean:
    def __init__(self, weight: int, e: Tuple[int,int], Ne0_e1: Set[int], Ne0e1: Set[int], Ne1_e0: Set[int], f: int) -> None:
        self.weight = weight
        self.e = e
        self.Ne0_e1 = Ne0_e1
        self.Ne0e1 = Ne0e1
        self.Ne1_e0 = Ne1_e0
        self.old_f = f
        self.f = f

    def adjust_f(self):
        self.old_f = self.f

    def delete_v_out_Ne0_e1(self, v: int):
        self.Ne0_e1.remove(v)

    def delete_v_out_Ne1_e0(self, v: int):
        self.Ne1_e0.remove(v)

    def delete_v_in(self, v: int):
        self.Ne0e1.remove(v)

    def delete_v_out_Ne0_e1_f(self, G: nx.Graph, v: int):
        self.Ne0_e1.remove(v)
        self.f -= G[self.e[0]][v]["EdgeBean"].weight

    def delete_v_out_Ne1_e0_f(self, G: nx.Graph, v: int):
        self.Ne1_e0.remove(v)
        self.f -= G[self.e[1]][v]["EdgeBean"].weight

    def add_v_out_Ne0_e1(self, G: nx.Graph, v: int):
        self.Ne0_e1.add(v)
        self.f += G[self.e[0]][v]["EdgeBean"].weight

    def add_v_out_Ne1_e0(self, G: nx.Graph, v: int):
        self.Ne1_e0.add(v)
        self.f += G[self.e[1]][v]["EdgeBean"].weight

    def print_EdgeBean(self):
        print("weight ", self.weight)
        print("e0 {} e1 {}".format(self.e[0], self.e[1]))
        print("Ne0_e1 ", self.Ne0_e1)
        print("Ne0e1 ", self.Ne0e1)
        print("Ne1_e0 ", self.Ne1_e0)
        print("olf_f {} f {}".format(self.old_f, self.f))

    def merge(self, edgeBean, G: nx.Graph) -> bool:
        # self.weight += edgeBean.weight
        self.Ne0e1 &= edgeBean.Ne0e1

        if self.e[1] == edgeBean.e[1]:
            self.Ne0_e1 &= edgeBean.Ne0_e1
            self.Ne1_e0 |= edgeBean.Ne1_e0
        elif self.e[0] == edgeBean.e[0]:
            self.Ne1_e0 &= edgeBean.Ne1_e0
            self.Ne0_e1 |= edgeBean.Ne0_e1
        elif self.e[0] == edgeBean.e[1]:
            self.Ne1_e0 &= edgeBean.Ne0_e1
            self.Ne0_e1 |= edgeBean.Ne1_e0
        else:
            self.Ne0_e1 &= edgeBean.Ne1_e0
            self.Ne1_e0 |= edgeBean.Ne0_e1
        self.f = f_with_edgeBean(self, G)

        return True if self.old_f != self.f else False


class RangedHeap:
    def __init__(self, G: nx.Graph) -> None:
        self.size = len(G.edges)
        # self.fs = [set() for _ in range(len(G.nodes))]
        self.fs = [set() for _ in range(self.size)]
        self.bool_fs = []

        for e in G.edges:
            e = get_e(e[0],e[1])
            Ne0_e1, Ne0e1, Ne1_e0 = split_neighborhood(G, e)
            val = len(Ne0_e1) + len(Ne1_e0)
            self.fs[val].add(e)
            G[e[0]][e[1]]['EdgeBean'] = EdgeBean(
                1, e, Ne0_e1, Ne0e1, Ne1_e0, val)

        for id, id_map in enumerate(self.fs):
            if len(id_map) != 0:
                self.bool_fs.append(id)

    def getMin(self, G: nx.Graph) -> EdgeBean:
        if self.size >= 1:
            e = self.getMinTwins(G)
            # out = self.fs[self.bool_fs[0]].popitem()[1]
            self.size -= 1
            f_val = self.bool_fs[0]
            if len(self.fs[f_val]) == 0:
                del self.bool_fs[0]

            return G[e[0]][e[1]]['EdgeBean']
        else:
            print("RangedHeap is empty")

    def get_f_Min(self):
        return self.bool_fs[0]

    def getMinTwins(self, G):
        weight_max = -math.inf
        edge_to_pick = None
        for e in self.fs[self.bool_fs[0]]:
            w = G[e[0]][e[1]]['EdgeBean'].weight
            if weight_max < w:
                weight_max = w
                edge_to_pick = e
        self.fs[self.bool_fs[0]].remove(edge_to_pick)
        return edge_to_pick

    # def getMinTwins(self, G):
    #     val_max = -math.inf
    #     edge_to_pick = None
    #     for e in self.fs[self.bool_fs[0]]:
    #         edgeBean_e = G[e[0]][e[1]]['EdgeBean']
    #         b = f_B(G, edgeBean_e) + edgeBean_e.weight
    #         norm = b + edgeBean_e.f
    #         w = b / norm
    #         if val_max < w:
    #             val_max = w
    #             edge_to_pick = e
    #         # elif weight_max == w:
    #         #     if edge_to_pick[0] < e[0]:
    #         #         edge_to_pick = e
    #     self.fs[self.bool_fs[0]].remove(edge_to_pick)
    #     return edge_to_pick

    def delete_e(self, e, f):
        self.fs[f].remove(e)
        self.size -= 1

        if len(self.fs[f]) == 0:
            self.binary_search_delete(f)

    def add(self, e, f):
        if len(self.fs[f]) == 0:
            self.binary_search_add(f)
        self.fs[f].add(e)
        self.size += 1

    def adjust(self, edgeBean):
        self.fs[edgeBean.old_f].remove(edgeBean.e)

        if len(self.fs[edgeBean.old_f]) == 0:
            self.binary_search_delete(edgeBean.old_f)
            
        if len(self.fs[edgeBean.f]) == 0:
            self.binary_search_add(edgeBean.f)

        self.fs[edgeBean.f].add(edgeBean.e)

        edgeBean.adjust_f()

    def merge_and_add(self, G, edgeBean1, edgeBean2):
        self.delete_e(edgeBean2.e, edgeBean2.f)

        if edgeBean1.merge(edgeBean2, G):
            self.adjust(edgeBean1)

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
        if len(self.bool_fs) == 0:
            self.bool_fs.append(x)
        elif x < self.bool_fs[0]:
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

    def print_fs(self):
        for id, id_map in enumerate(self.fs):
            edges = ""
            for edge in id_map:
                edges += " " + str(edge)
            s = "[" + str(id) + "]->" + edges + "\n"
            print(s)

    def prinf_bool_fs(self):
        print(self.bool_fs)

    def print_rangedHeap(self):
        self.print_fs()
        self.prinf_bool_fs()

    def __len__(self):
        return self.size


# def preprocess(G: nx.Graph) -> Tuple[int, int]:
#     nx.set_node_attributes(G, None, "clique")
#     nx.set_edge_attributes(G, None, "EdgeBean")

#     for node in G.nodes:
#         G.nodes[node]["clique"] = set([node])

#     rangedHeap = RangedHeap(G)
#     value = 0
#     while True:
#         if rangedHeap.get_f_Min() > 0:
#             break
#         edgeBean = rangedHeap.getMin(G)
#         value += 1
#         edge_contraction(G, edgeBean, rangedHeap)
#     return value, len(rangedHeap)


def split_neighborhood(G: nx.Graph, e: Tuple[int, int]) -> Tuple[Set[int], Set[int], Set[int]]:
    vicini0 = set(G.neighbors(e[0]))
    vicini0.remove(e[1])
    vicini1 = set(G.neighbors(e[1]))
    vicini1.remove(e[0])

    return vicini0 - vicini1, vicini0 & vicini1, vicini1 - vicini0


def f_with_edgeBean(edgeBean: EdgeBean, G: nx.Graph) -> int:
    value = 0

    for node in edgeBean.Ne0_e1:  # removed
        value += G[edgeBean.e[0]][node]['EdgeBean'].weight

    for node in edgeBean.Ne1_e0:  # removed
        value += G[edgeBean.e[1]][node]['EdgeBean'].weight

    return value


def edge_contraction(G, egBean: EdgeBean, rangedHeap: RangedHeap):
    for node in egBean.Ne0_e1:  # removed
        edgeBean = G[egBean.e[0]][node]["EdgeBean"]
        rangedHeap.delete_e(edgeBean.e, edgeBean.f)

    for node in egBean.Ne1_e0:  # removed
        edgeBean = G[egBean.e[1]][node]["EdgeBean"]
        rangedHeap.delete_e(edgeBean.e, edgeBean.f)

    toAdjust_in_rangedHeap = set()

    adjust_edge_Ne0e1(G, egBean.e[0], egBean.e[1], 
                      egBean.Ne0e1, egBean.Ne0_e1,
                      egBean.Ne1_e0, toAdjust_in_rangedHeap)
    adjust_edge_Ne0_e1(G, egBean.e[0], egBean.Ne0_e1,
                       egBean.Ne0e1, toAdjust_in_rangedHeap)
    adjust_edge_Ne1_e0(G, egBean.e[1], egBean.Ne1_e0, 
                       egBean.Ne0e1, toAdjust_in_rangedHeap)

    for node in egBean.Ne0e1:
        G[egBean.e[0]][node]['EdgeBean'].weight += G[egBean.e[1]][node]['EdgeBean'].weight

    for node in egBean.Ne0e1:
        edgeBean1 = G[egBean.e[0]][node]["EdgeBean"]
        edgeBean2 = G[egBean.e[1]][node]["EdgeBean"]
        rangedHeap.merge_and_add(G, edgeBean1, edgeBean2)

    for edge in toAdjust_in_rangedHeap:
        edgeBean = G[edge[0]][edge[1]]["EdgeBean"]
        rangedHeap.adjust(edgeBean)

    for node in egBean.Ne0_e1:  # removed
        G.remove_edge(egBean.e[0], node)

    G.nodes[egBean.e[0]]["clique"] |= G.nodes[egBean.e[1]]["clique"]
    G.remove_node(egBean.e[1])


def adjust_edge_Ne0_e1(G: nx.Graph, e0: int, Ne0_e1: Set[int], Ne0e1: Set[int], toAdjust_in_rangedHeap: Set[Tuple[int, int]]):
    toAdjust_Ne0_e1 = G.edges(list(Ne0_e1))

    # eliminare dai vicini e[0] e nel caso sta in A,C allora occorre modificare f altrimenti niente
    for edge in toAdjust_Ne0_e1:
        if edge[0] != e0 and edge[1] != e0:
            if edge[0] in Ne0_e1:
                a = edge[0]
                other = edge[1]
            else:
                a = edge[1]
                other = edge[1]

            edgeBean = G[edge[0]][edge[1]]["EdgeBean"]

            if other in Ne0_e1 or other in Ne0e1:                       # A - A or A - B
                edgeBean.delete_v_in(e0)
            else:                                                       # A - C or A - ext
                if edgeBean.e[0] == a:
                    edgeBean.delete_v_out_Ne0_e1_f(G, e0)
                else:
                    edgeBean.delete_v_out_Ne1_e0_f(G, e0)
                toAdjust_in_rangedHeap.add(edge)


def adjust_edge_Ne0e1(G: nx.Graph, e0: int, e1: int, Ne0e1: Set[int], Ne0_e1: Set[int], Ne1_e0: Set[int], toAdjust_in_rangedHeap: Set[Tuple[int, int]]):
    toAdjust_Ne0e1 = G.edges(list(Ne0e1))

    for edge in toAdjust_Ne0e1:
        # REMOVE e[1] dagl'insiemi
        if edge[0] != e0 and edge[1] != e0 and edge[0] != e1 and edge[1] != e1:
            if edge[0] in Ne0e1:
                b = edge[0]
                other = edge[1]
            else:
                b = edge[1]
                other = edge[0]

            edgeBean = G[edge[0]][edge[1]]["EdgeBean"]

            if other in Ne0_e1:                                         # B - A
                if edgeBean.e[0] == b:
                    edgeBean.delete_v_out_Ne0_e1(e1)
                    edgeBean.add_v_out_Ne0_e1(G, e0)
                else:
                    edgeBean.delete_v_out_Ne1_e0(e1)
                    edgeBean.add_v_out_Ne1_e0(G, e0)
                toAdjust_in_rangedHeap.add(edge)
            elif other in Ne0e1:                                        # B - B
                edgeBean.delete_v_in(e1)
            elif other in Ne1_e0:                                       # B - C
                edgeBean.f += G[e1][b]["EdgeBean"].weight
                toAdjust_in_rangedHeap.add(edge)
            else:                                                       # B - ext
                if edgeBean.e[0] == b:
                    edgeBean.delete_v_out_Ne0_e1(e1)
                else:
                    edgeBean.delete_v_out_Ne1_e0(e1)


def adjust_edge_Ne1_e0(G: nx.Graph, e1: int, Ne1_e0: Set[int], Ne0e1: Set[int], toAdjust_in_rangedHeap: Set[Tuple[int, int]]):
    # eliminare dai vicini e[0] e nel caso sta in A,C allora occorre modificare f altrimenti niente
    for edge in G.edges(list(Ne1_e0)):
        if edge[0] != e1 and edge[1] != e1:
            if edge[0] in Ne1_e0:
                c = edge[0]
                other = edge[1]
            else:
                c = edge[1]
                other = edge[0]

            # REMOVE e1 dagl'insiemi
            edgeBean = G[edge[0]][edge[1]]["EdgeBean"]

            if other in Ne0e1 or other in Ne1_e0:                   # C - B or C - C
                edgeBean.delete_v_in(e1)
            else:                                                   # C - A or C - ext
                if edgeBean.e[0] == c:
                    edgeBean.delete_v_out_Ne0_e1_f(G, e1)
                else:
                    edgeBean.delete_v_out_Ne1_e0_f(G, e1)
                toAdjust_in_rangedHeap.add(edge)


def deleted_edge_greedy(G):
    nx.set_node_attributes(G, None, "clique")
    nx.set_edge_attributes(G, None, "EdgeBean")

    for node in G.nodes:
        G.nodes[node]["clique"] = set([node])

    rangedHeap = RangedHeap(G)

    sol_val = 0

    while len(rangedHeap) != 0:
        edgeBean = rangedHeap.getMin(G)
        sol_val += edgeBean.f
        edge_contraction(G, edgeBean, rangedHeap)

    return sol_val
