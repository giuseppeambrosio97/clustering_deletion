import time
import warnings
import cplex
import networkx as nx
from matplotlib import MatplotlibDeprecationWarning

import matplotlib.pyplot as plt

from instance_reducer import reduce
from io_func import readGraph_n_m, readGraph_m, readGraph_comma


class CplexCliqueClusteringModel1:

    def __init__(self,
                 G:nx.Graph,
                 verbose=False):

        self.G = G
        self.verbose = verbose

        # Create the model
        self.cpx = cplex.Cplex()

        # Create variables

        self.x = {}

        for e in self.G.edges:
            i = e[0]
            j = e[1]
            self.x[(i, j) if i < j else (j, i)] = self.cpx.variables.add(
                obj=[1],
                lb=[0.0],
                ub=[1.0],
                types=[self.cpx.variables.type.binary],
                names=["x({},{})".format(i, j) if i<j else "x({},{})".format(j, i)]
            ).start

        self.cpx.objective.set_sense(self.cpx.objective.sense.maximize)

        self.objCoefficients = self.cpx.objective.get_linear()

        if self.verbose:
            print("Variables and objective defined")

        # constraints
        for i in self.G.nodes:
            for j in self.G[i]:
                for k in self.G[i]:
                    if j < k:
                        if self.G.has_edge(j,k):
                            left_hand_2 = [cplex.SparsePair([
                                self.cpx.variables.get_indices("x({},{})".format(j, k) if j<k else "x({},{})".format(k, j)),
                                self.cpx.variables.get_indices("x({},{})".format(i, j) if i<j else "x({},{})".format(j, i)),
                                self.cpx.variables.get_indices("x({},{})".format(i, k) if i<k else "x({},{})".format(k, i))
                            ], [-1.0, 1.0, 1.0])]

                            self.cpx.linear_constraints.add(lin_expr=left_hand_2,
                                                            senses=['L'],
                                                            rhs=[1])
                        else:
                            left_hand_2 = [cplex.SparsePair([
                                self.cpx.variables.get_indices("x({},{})".format(i, j) if i < j else "x({},{})".format(j, i)),
                                self.cpx.variables.get_indices("x({},{})".format(i, k) if i < k else "x({},{})".format(k, i))
                            ], [1.0, 1.0])]

                            self.cpx.linear_constraints.add(lin_expr=left_hand_2,
                                                            senses=['L'],
                                                            rhs=[1])

        self.tol = self.cpx.parameters.mip.tolerances.integrality.get()

        if verbose:
            print("Constraints defined")

        self.cpx.parameters.threads.set(1)
        self.cpx.parameters.timelimit.set(3600*12)

    def solve(self):

        # self.cpx.write('model1.lp')

        solve_start = time.time()
        self.cpx.solve()
        solve_time = time.time() - solve_start

        obj = -1
        edges_selected = []

        if self.cpx.solution.get_status() == 103:
            if self.verbose:
                print("Infeasible")
            output = {
                "status": self.cpx.solution.get_status(),
                "solveTime": solve_time,
                "objValue": obj
            }
            return output

        if self.cpx.solution.get_status() != 108 and self.cpx.solution.get_status() != '108':
            obj = self.cpx.solution.get_objective_value()
            if self.verbose:
                print('Optimal value:                     %f' % self.cpx.solution.get_objective_value())

            values = self.cpx.solution.get_values()
            for e in self.x:
                if values[self.x.get(e)] >= 1 - self.tol:
                    # if self.verbose:
                    print("{} selected".format(e), "--->", values[self.x.get(e)])
                    edges_selected.append(e)

            output = {
                "status": self.cpx.solution.get_status(),
                "solveTime": solve_time,
                "objValue": obj,
                "edgesSelected": edges_selected
            }

            return output
        else:
            if self.verbose:
                print("Infeasible")
            output = {
                "status": self.cpx.solution.get_status(),
                "solveTime": solve_time,
                "objValue": obj
            }
            return output


    def is_feasible(self, edges_selected):
        induced_graph = nx.Graph()
        for e in edges_selected:
            induced_graph.add_edge(e[0], e[1])
        color_map = []
        for edge in induced_graph.edges:
            if edge in edges_selected or (edge[1], edge[0]) in edges_selected:
                color_map.append('xkcd:coral')
            else:
                print("bah", edge)
                color_map.append('xkcd:grey')

        # nx.draw(induced_graph, edge_color=color_map, with_labels=True, font_weight='bold')
        # plt.show()

        for cc in nx.connected_components(induced_graph):
            # print(cc, sum([1 for ee in edges_selected if ee[0] in cc and ee[1] in cc]))
            is_clique = sum([1 for ee in edges_selected if ee[0] in cc and ee[1] in cc]) == len(cc)*(len(cc)-1)/2
            if is_clique:
                # print("Component {} is a clique".format(cc))
                continue
            else:
                return False
                # print("Component {} is NOT a clique".format(cc))

        return True


if __name__ == "__main__":

    G = readGraph_m("./Instances_Hidden_Cliques_Small/HC_15_10_0.3.txt")

    # edge_selected = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 82), (0, 90), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 103), (1, 136), (1, 101), (1, 132), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 89), (2, 38), (2, 134), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 21), (3, 49), (3, 91), (3, 107), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 100), (5, 6), (5, 7), (5, 8), (5, 9), (5, 99), (5, 86), (5, 101), (6, 7), (6, 8), (6, 9), (6, 63), (6, 99), (6, 100), (6, 139), (6, 38), (6, 134), (6, 96), (7, 8), (7, 9), (7, 114), (7, 121), (7, 135), (8, 9), (8, 90), (8, 91), (8, 138), (8, 137), (8, 110), (8, 46), (9, 19), (9, 52), (9, 38), (9, 64), (16, 19), (16, 29), (16, 17), (16, 41), (16, 18), (19, 113), (19, 92), (21, 23), (21, 29), (21, 112), (21, 26), (21, 27), (21, 28), (21, 24), (21, 25), (21, 22), (21, 80), (21, 123), (23, 29), (23, 58), (23, 83), (23, 112), (23, 127), (23, 138), (23, 26), (23, 27), (23, 28), (23, 24), (23, 25), (23, 74), (23, 81), (29, 50), (44, 45), (44, 47), (44, 49), (44, 46), (44, 48), (45, 47), (45, 49), (45, 46), (45, 48), (47, 49), (47, 103), (47, 48), (49, 73), (49, 131), (53, 57), (53, 58), (53, 59), (53, 54), (53, 105), (53, 93), (53, 126), (53, 149), (53, 56), (53, 55), (57, 58), (57, 59), (57, 78), (57, 112), (57, 98), (57, 84), (57, 80), (58, 59), (58, 69), (58, 82), (58, 83), (58, 60), (58, 101), (58, 129), (58, 108), (58, 119), (58, 106), (59, 82), (59, 118), (61, 62), (61, 63), (61, 65), (61, 66), (61, 67), (61, 69), (61, 68), (61, 64), (62, 63), (62, 65), (62, 66), (62, 67), (62, 69), (62, 68), (62, 64), (63, 65), (63, 66), (63, 67), (63, 69), (63, 130), (63, 68), (63, 64), (63, 131), (65, 66), (65, 67), (65, 69), (65, 128), (65, 68), (65, 137), (65, 109), (66, 67), (66, 69), (66, 68), (67, 69), (67, 68), (69, 90), (69, 139), (69, 147), (69, 145), (71, 77), (71, 78), (71, 130), (71, 141), (71, 73), (71, 76), (71, 79), (71, 134), (71, 137), (71, 74), (71, 109), (71, 75), (71, 72), (77, 78), (77, 79), (78, 79), (78, 110), (78, 145), (82, 83), (82, 88), (82, 89), (82, 128), (82, 86), (82, 87), (82, 84), (82, 85), (83, 88), (83, 89), (83, 99), (83, 128), (83, 86), (83, 87), (83, 101), (83, 93), (83, 84), (83, 147), (83, 85), (88, 89), (88, 91), (88, 138), (88, 131), (89, 112), (89, 145), (90, 91), (90, 99), (90, 128), (90, 130), (90, 94), (90, 98), (90, 92), (90, 93), (90, 95), (90, 97), (90, 96), (91, 99), (91, 94), (91, 98), (91, 139), (91, 92), (91, 93), (91, 95), (91, 142), (91, 97), (91, 96), (99, 107), (99, 106), (102, 103), (102, 105), (102, 107), (102, 104), (102, 108), (102, 109), (102, 106), (103, 105), (103, 107), (103, 104), (103, 108), (103, 109), (103, 106), (112, 113), (112, 114), (112, 118), (112, 116), (112, 117), (112, 119), (112, 115), (113, 114), (113, 118), (113, 116), (113, 117), (113, 119), (113, 148), (113, 115), (114, 118), (114, 120), (114, 116), (114, 122), (114, 117), (114, 119), (114, 115), (118, 119), (118, 126), (120, 121), (120, 127), (120, 128), (120, 122), (120, 125), (120, 129), (120, 140), (120, 126), (120, 124), (120, 123), (121, 127), (121, 128), (121, 122), (121, 125), (121, 129), (121, 126), (121, 131), (121, 147), (121, 145), (121, 124), (121, 123), (127, 128), (127, 129), (127, 149), (128, 129), (128, 131), (130, 133), (130, 135), (130, 136), (130, 138), (130, 132), (130, 139), (130, 134), (130, 137), (130, 131), (133, 135), (133, 136), (133, 138), (133, 139), (133, 134), (133, 137), (135, 136), (135, 138), (135, 144), (135, 139), (135, 137), (136, 138), (136, 139), (136, 137), (136, 142), (138, 139), (141, 144), (141, 146), (141, 142), (141, 148), (141, 149), (141, 143), (141, 147), (141, 145), (144, 146), (144, 148), (144, 149), (144, 147), (144, 145), (146, 148), (146, 149), (146, 147), (10, 16), (10, 19), (10, 120), (10, 11), (10, 17), (10, 107), (10, 14), (10, 13), (10, 15), (10, 37), (10, 12), (10, 18), (11, 16), (11, 19), (11, 49), (11, 120), (11, 17), (11, 14), (11, 95), (11, 137), (11, 109), (11, 13), (11, 15), (11, 41), (11, 84), (11, 43), (11, 12), (11, 18), (17, 19), (17, 136), (17, 18), (26, 29), (26, 102), (26, 27), (26, 28), (26, 36), (26, 51), (27, 29), (27, 130), (27, 136), (27, 28), (27, 134), (27, 123), (28, 29), (28, 124), (28, 123), (36, 69), (36, 82), (36, 39), (36, 38), (36, 37), (36, 70), (39, 136), (39, 146), (39, 132), (39, 75), (51, 53), (51, 57), (51, 58), (51, 59), (51, 52), (51, 54), (51, 86), (51, 92), (51, 117), (51, 142), (51, 56), (51, 84), (51, 55), (52, 53), (52, 57), (52, 58), (52, 59), (52, 67), (52, 77), (52, 130), (52, 54), (52, 104), (52, 56), (52, 81), (52, 55), (52, 123), (54, 57), (54, 58), (54, 59), (54, 90), (54, 56), (54, 97), (54, 55), (60, 61), (60, 62), (60, 63), (60, 65), (60, 66), (60, 67), (60, 69), (60, 113), (60, 68), (60, 134), (60, 64), (73, 77), (73, 78), (73, 120), (73, 136), (73, 144), (73, 76), (73, 79), (73, 74), (73, 75), (73, 131), (76, 77), (76, 78), (76, 88), (76, 102), (76, 79), (76, 125), (76, 104), (79, 116), (79, 93), (79, 134), (79, 131), (86, 88), (86, 89), (86, 87), (86, 139), (86, 147), (87, 88), (87, 89), (87, 144), (94, 99), (94, 98), (94, 95), (94, 126), (94, 97), (94, 96), (94, 143), (98, 99), (98, 110), (98, 123), (100, 102), (100, 103), (100, 101), (100, 105), (100, 107), (100, 104), (100, 108), (100, 109), (100, 106), (101, 102), (101, 103), (101, 105), (101, 107), (101, 104), (101, 108), (101, 109), (101, 115), (101, 106), (101, 145), (105, 107), (105, 108), (105, 109), (105, 106), (105, 143), (107, 108), (107, 109), (107, 110), (116, 118), (116, 117), (116, 119), (122, 127), (122, 128), (122, 125), (122, 129), (122, 126), (122, 124), (122, 123), (125, 127), (125, 128), (125, 129), (125, 126), (125, 145), (129, 131), (132, 133), (132, 135), (132, 136), (132, 138), (132, 139), (132, 134), (132, 137), (140, 141), (140, 144), (140, 146), (140, 142), (140, 148), (140, 149), (140, 143), (140, 147), (140, 145), (14, 16), (14, 19), (14, 89), (14, 91), (14, 146), (14, 17), (14, 28), (14, 15), (14, 18), (24, 29), (24, 26), (24, 27), (24, 28), (24, 25), (32, 45), (32, 36), (32, 39), (32, 87), (32, 34), (32, 38), (32, 108), (32, 35), (32, 37), (32, 33), (32, 145), (34, 136), (34, 36), (34, 39), (34, 38), (34, 35), (34, 37), (34, 55), (38, 69), (38, 39), (38, 126), (38, 115), (68, 69), (68, 81), (92, 99), (92, 120), (92, 121), (92, 144), (92, 94), (92, 98), (92, 93), (92, 95), (92, 97), (92, 96), (93, 99), (93, 94), (93, 98), (93, 95), (93, 97), (93, 96), (95, 99), (95, 98), (95, 140), (95, 134), (95, 109), (95, 97), (95, 96), (104, 112), (104, 105), (104, 107), (104, 125), (104, 108), (104, 109), (104, 106), (108, 117), (108, 148), (108, 109), (117, 118), (117, 122), (117, 139), (117, 119), (119, 134), (119, 142), (126, 127), (126, 128), (126, 129), (134, 135), (134, 136), (134, 138), (134, 139), (134, 137), (137, 138), (137, 139), (142, 144), (142, 146), (142, 148), (142, 149), (142, 143), (142, 147), (142, 145), (148, 149), (25, 29), (25, 26), (25, 27), (25, 28), (42, 44), (42, 45), (42, 47), (42, 49), (42, 43), (42, 46), (42, 48), (50, 53), (50, 57), (50, 58), (50, 59), (50, 127), (50, 51), (50, 52), (50, 54), (50, 56), (50, 55), (56, 57), (56, 58), (56, 59), (56, 90), (56, 108), (56, 147), (56, 85), (74, 77), (74, 78), (74, 121), (74, 76), (74, 79), (74, 137), (74, 115), (74, 75), (81, 82), (81, 83), (81, 88), (81, 89), (81, 103), (81, 121), (81, 86), (81, 87), (81, 109), (81, 84), (81, 147), (81, 85), (109, 135), (109, 126), (109, 111), (110, 112), (110, 113), (110, 114), (110, 118), (110, 116), (110, 117), (110, 119), (110, 149), (110, 111), (110, 115), (111, 112), (111, 113), (111, 114), (111, 118), (111, 135), (111, 116), (111, 117), (111, 119), (111, 115), (115, 118), (115, 116), (115, 129), (115, 117), (115, 119), (13, 16), (13, 19), (13, 141), (13, 17), (13, 14), (13, 104), (13, 74), (13, 109), (13, 15), (13, 18), (15, 16), (15, 19), (15, 17), (15, 68), (15, 131), (15, 18), (31, 103), (31, 36), (31, 39), (31, 94), (31, 132), (31, 32), (31, 34), (31, 38), (31, 56), (31, 35), (31, 37), (31, 33), (31, 48), (35, 69), (35, 36), (35, 39), (35, 38), (35, 37), (35, 85), (37, 39), (37, 38), (41, 44), (41, 45), (41, 47), (41, 49), (41, 42), (41, 43), (41, 46), (41, 145), (41, 48), (84, 88), (84, 89), (84, 113), (84, 128), (84, 133), (84, 86), (84, 87), (84, 129), (84, 85), (97, 99), (97, 98), (97, 119), (20, 21), (20, 23), (20, 29), (20, 77), (20, 26), (20, 27), (20, 28), (20, 129), (20, 24), (20, 25), (20, 22), (22, 23), (22, 29), (22, 62), (22, 77), (22, 114), (22, 26), (22, 27), (22, 28), (22, 122), (22, 24), (22, 34), (22, 25), (30, 99), (30, 103), (30, 36), (30, 39), (30, 32), (30, 34), (30, 38), (30, 149), (30, 110), (30, 31), (30, 35), (30, 37), (30, 33), (30, 85), (55, 57), (55, 58), (55, 59), (55, 98), (55, 139), (55, 56), (70, 71), (70, 77), (70, 78), (70, 73), (70, 76), (70, 79), (70, 148), (70, 74), (70, 75), (70, 72), (75, 77), (75, 78), (75, 76), (75, 79), (75, 80), (80, 82), (80, 83), (80, 88), (80, 89), (80, 86), (80, 87), (80, 105), (80, 93), (80, 95), (80, 117), (80, 81), (80, 84), (80, 85), (72, 77), (72, 78), (72, 73), (72, 76), (72, 79), (72, 140), (72, 134), (72, 74), (72, 75), (96, 99), (96, 144), (96, 98), (96, 125), (96, 97), (96, 106), (96, 124), (106, 127), (106, 130), (106, 107), (106, 108), (106, 137), (106, 109), (106, 123), (33, 36), (33, 39), (33, 34), (33, 38), (33, 35), (33, 37), (33, 75), (33, 131), (40, 44), (40, 45), (40, 47), (40, 49), (40, 77), (40, 92), (40, 42), (40, 41), (40, 43), (40, 46), (40, 48), (43, 44), (43, 45), (43, 47), (43, 49), (43, 91), (43, 46), (43, 48), (46, 47), (46, 49), (46, 87), (46, 48), (64, 65), (64, 66), (64, 67), (64, 69), (64, 139), (64, 68), (64, 126), (64, 137), (64, 145), (131, 133), (131, 135), (131, 136), (131, 138), (131, 141), (131, 144), (131, 132), (131, 139), (131, 134), (131, 137), (143, 144), (143, 146), (143, 148), (143, 149), (143, 147), (143, 145), (147, 148), (147, 149), (85, 88), (85, 89), (85, 86), (85, 87), (85, 134), (85, 109), (145, 146), (145, 148), (145, 149), (145, 147), (12, 16), (12, 19), (12, 103), (12, 135), (12, 17), (12, 14), (12, 81), (12, 13), (12, 15), (12, 97), (12, 18), (12, 124), (18, 19), (18, 60), (18, 68), (18, 104), (18, 137), (18, 110), (48, 49), (48, 121), (48, 132), (124, 127), (124, 128), (124, 125), (124, 129), (124, 126), (123, 127), (123, 128), (123, 125), (123, 129), (123, 126), (123, 149), (123, 124)]

    # model = CplexCliqueClusteringModel1(G, verbose=False)

    # resfeas = model.is_feasible(edges_selected=edge_selected)
    # print("is_feasible?", resfeas)
    # exit(0)

    # G = readGraph_n_m("test_90_1345_90675_1.txt")
    # G = nx.random_tree(n=50)
    # G = nx.dense_gnm_random_graph(n=20, m=150)
    # G = readGraph_m("./datasets/bio-HS-HT.edges") # out of memory
    # G = readGraph_comma("./datasets/bio-grid-worm.edges")


    # reduce(G, 500)

    print("Nodes ({}):".format(G.number_of_nodes()), G.nodes)
    print("Edges ({}):".format(G.number_of_edges()), G.edges(data=True))

    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()

    model = CplexCliqueClusteringModel1(G, verbose=False)

    start_time = time.time()
    print("Start time:", start_time)
    output = model.solve()
    print(">>>>>> CPLEX clique clustering model TIME:", time.time() - start_time)
    print(output)

    if int(output.get("status")) == 101:
        color_map = []
        for edge in G.edges:
            if edge in output.get("edgesSelected") or (edge[1], edge[0]) in output.get("edgesSelected"):
                color_map.append('xkcd:coral')
            else:
                color_map.append('xkcd:grey')

        nx.draw(G, edge_color=color_map, with_labels=True, font_weight='bold')
        plt.show()
        print("Feasible?", model.is_feasible(edges_selected=output.get("edgesSelected")))

