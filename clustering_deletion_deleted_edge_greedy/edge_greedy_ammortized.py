import math


class RangedHeap:
    def __init__(self, G):
        self.size = len(G.edges)
        self.fs = [{} for _ in range(len(G.nodes))]
        self.current_min = -1

        for e in G.edges:
            val = f(G, e)
            G[e[0]][e[1]]['f'] = val
            e = self.get_e(e[0], e[1])
            self.fs[val][e] = e
        
        for id, id_map in enumerate(self.fs):
            if len(id_map) != 0:
                self.current_min = id
                break

    def getMin(self, G):
        if self.size >= 1:
            out = self.getMinTwins(G)
            # out = self.fs[self.bool_fs[0]].popitem()[1]
            self.size -= 1
            return out
        else:
            print("RangedHeap is empty")

    def getMinTwins(self, G):
        weight_max = -math.inf
        edge_to_pick = None
        if len(self.fs[self.current_min]) == 0:
            for i in range(self.current_min+1,len(self.fs)):
                if len(self.fs[i]) != 0:
                    self.current_min = i
                    break

        for _,e in self.fs[self.current_min].items():
            w = G[e[0]][e[1]]['weight']
            if weight_max < w:
                weight_max = w
                edge_to_pick = e
        del self.fs[self.current_min][edge_to_pick]
        return edge_to_pick

    def delete_e(self, e0, e1, f):
        e = self.get_e(e0, e1)
        del self.fs[f][e]
        self.size -= 1

        # if len(self.fs[f]) == 0:
        #     self.binary_search_delete(f)

    def add(self, e0, e1, f):
        e = self.get_e(e0, e1)
        # if len(self.fs[f]) == 0:
        #     self.binary_search_add(f)
        if f < self.current_min:
            self.current_min = f
        self.fs[f][e] = e
        self.size += 1

    def adjust(self, e0, e1, old_f, new_f):
        e = self.get_e(e0, e1)
        self.delete_e(e[0], e[1], old_f)
        self.add(e[0], e[1], new_f)


    def get_e(self, e0, e1):
        return (e0, e1) if int(e0) < int(e1) else (e1, e0)

    def print_fs(self):
        for id, id_map in enumerate(self.fs):
            values = ""
            for key, value in id_map.items():
                values += " " + str(value)
            s = "[" + str(id) + "]->" + values + "\n"
            print(s)


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


def clustering_deleteting_choice_deleted_edge_greedy(G):
    rangedHeap = RangedHeap(G)
    value = 0
    while len(rangedHeap) != 0:
        e = rangedHeap.getMin(G)
        value += G[e[0]][e[1]]['f']
        edge_contraction(G, e, rangedHeap)
    return value
