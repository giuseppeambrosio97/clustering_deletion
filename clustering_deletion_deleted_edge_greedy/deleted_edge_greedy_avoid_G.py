import math


class EdgeBean:
    def __init__(self, weight,e0,e1, Ne0_e1, Ne0e1, Ne1_e0, f) -> None:
        self.weight = weight
        self.e0 = e0
        self.e1 = e1
        self.Ne0_e1 = Ne0_e1
        self.Ne0e1 = Ne0e1
        self.Ne1_e0 = Ne1_e0
        self.f = f
    
    def delete_Ne0_e1_node(self, v):
        self.Ne0_e1.remove(v)

    def add_Ne0_e1_node(self,v):
        self.Ne0_e1.add(v)

    def delete_Ne1_e0_node(self, v):
        self.Ne1_e0.remove(v)

    def add_Ne1_e0_node(self, v):
        self.Ne1_e0.add(v)

    def delete_Ne0e1_node(self, v):
        self.Ne0e1.remove(v)

    def add_Ne0e1_node(self, v):
        self.Ne0e1.add(v)

    def delete_v(self, G, v):
        """
            return True se l'edge è da sistemare nella rangedHeap
        """
        if v in self.Ne0_e1:
            self.Ne0_e1.remove(v)
            G[self.e0][v]['f'] -= G[self.e0][v]['weight']
            return True
        elif v in self.Ne1_e0:
            self.Ne1_e0.remove(v)
            G[self.e1][v]['f'] -= G[self.e1][v]['weight']
            return True
        elif v in self.Ne0e1:
            self.Ne0e1.remove(v)
            return False
        else:
            print("ERRORE nodo non nel vicinato")
    



class RangedHeap:
    def __init__(self, G):
        self.size = len(G.edges)
        self.fs = [{} for _ in range(len(G.nodes))]
        self.bool_fs = []
        self.edge = {}

        for e in G.edges:
            e = self.get_e(e[0], e[1])
            Ne0_e1, Ne0e1, Ne1_e0 = split_neighborhood(G,e)
            val = f_with_sets(G,e,Ne0_e1,Ne1_e0)
            G[e[0]][e[1]]['f'] = val
            self.fs[val][e] = e
            G[e[0]][e[1]]['EdgeBean'] = EdgeBean(1, e[0],e[1],Ne0_e1, Ne0e1, Ne1_e0, val)
            # self.edges[e] = EdgeBean(1, Ne0_e1, Ne0e1, Ne1_e0, val)

        for id, id_map in enumerate(self.fs):
            if len(id_map) != 0:
                self.bool_fs.append(id)

    def getMin(self, G):
        if self.size >= 1:
            out = self.getMinTwins(G)
            # out = self.fs[self.bool_fs[0]].popitem()[1]
            self.size -= 1
            f_val = self.bool_fs[0]
            if len(self.fs[f_val]) == 0:
                del self.bool_fs[0]
            return out, f_val
        else:
            print("RangedHeap is empty")

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


    
    # def get_EdgeBean_e(self):
    #     return 

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


def preprocess(G):
    rangedHeap = RangedHeap(G)
    value = 0
    while True:
        e = rangedHeap.getMin(G)
        if(G[e[0]][e[1]]['f'] > 0):
            break
        edge_contraction(G, e, rangedHeap)
    return value


def xor(G, e):
    vicini0 = set(G.neighbors(e[0]))
    vicini0.remove(e[1])
    vicini1 = set(G.neighbors(e[1]))
    vicini1.remove(e[0])

    return vicini0 - vicini1, vicini1 - vicini0


def split_neighborhood(G, e):
    vicini0 = set(G.neighbors(e[0]))
    vicini0.remove(e[1])
    vicini1 = set(G.neighbors(e[1]))
    vicini1.remove(e[0])

    return vicini0 - vicini1, vicini0 & vicini1, vicini1 - vicini0


def f(G, e):
    Ne0_e1, Ne1_e0 = xor(G, e)
    value = 0

    for node in Ne0_e1:  # removed
        value += G[e[0]][node]['weight']

    for node in Ne1_e0:  # removed
        value += G[e[1]][node]['weight']

    return value


def f_with_sets(G, e, Ne0_e1, Ne1_e0):
    value = 0

    for node in Ne0_e1:  # removed
        value += G[e[0]][node]['weight']

    for node in Ne1_e0:  # removed
        value += G[e[1]][node]['weight']

    return value


def edge_contraction(G, e, rangedHeap):
    e = (e[0], e[1]) if int(e[0]) < int(e[1]) else (e[1], e[0])
    edgeBean = G[e[0]][e[1]]['EdgeBean']
    
    Ne0_e1, Ne0e1, Ne1_e0 = split_neighborhood(G, e)

    # Ne0_e1, Ne0e1, Ne1_e0 = edgeBean.Ne0_e1, edgeBean.Ne0e1, edgeBean.Ne1_e0

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



    toAdjust_Ne0_e1 = G.edges(list(Ne0_e1))

    for edge in toAdjust_Ne0_e1:
        # edgeBean_edge = G[edge[0]][edge[1]]['EdgeBean']
        # edgeBean_edge.delete(e[0])
        # rangedHeap.adjustNeighborhood_delete
        pass

    toAdjust = G.edges(list(Ne0e1)+list(Ne1_e0))


    # toAdjust = G.edges(list(Ne0_e1)+list(Ne0e1)+list(Ne1_e0))

    # toAdjust = G.edges(list(Ne0_e1)+list(Ne1_e0))
    for edge in toAdjust:
        if edge[0] != e[0] and edge[1] != e[0]:
            new_f = f(G, edge)
            old_f = G[edge[0]][edge[1]]['f']
            if new_f != old_f:
                G[edge[0]][edge[1]]['f'] = new_f
                rangedHeap.adjust(edge[0], edge[1], old_f, new_f)


def deleted_edge_greedy_avoid(G):
    rangedHeap = RangedHeap(G)
    sol_val = 0
    while len(rangedHeap) != 0:
        e, val = rangedHeap.getMin(G)
        sol_val+=val
        edge_contraction(G, e, rangedHeap)
    return sol_val
