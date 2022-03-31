import networkx as nx
import random as rnd

def random_generate_graph(nodes, edge_percentage, chance, path):
    possibilities = nodes*(nodes-1)/2
    number_to_add = possibilities * edge_percentage /100
    added = 0

    print("number to add", number_to_add)
    print("possibilities", possibilities)
    G = nx.Graph()
    nodi = [x for x in range(nodes)]
    G.add_nodes_from(nodi)
    while added < number_to_add:
        for i in range(len(nodi)-1):
            for j in range(i+1,len(nodi)):
                if not G.has_edge(nodi[i],nodi[j]) and rnd.randint(0,100) <= chance:
                    G.add_edge(nodi[i],nodi[j])
                    added+=1
                if added == number_to_add:
                    break
            if added == number_to_add:
                break

    f = open(path, "w")
    lines = ["{}\n".format(G.number_of_edges())]
    for e in G.edges:
        lines.append("{} {}\n".format(*e))
    f.writelines(lines)
    f.close()

def gen_battery_test(folder = "../Instances_random_new"):
    # Parametri large
    # numbers_of_nodes = [80, 110, 140, 170, 200]
    # edge_percentages = [50, 70, 80, 90]
    # chances = [30, 60, 90]
    numbers_of_nodes = [80, 110, 140, 170, 200]
    edge_percentages = [50, 70, 80, 90]
    chances = [30, 60, 90]
    for number_of_node in numbers_of_nodes:
        for edge_percentage in edge_percentages:
            for chance in chances:
                file_name = "{}_{}_{}.txt".format(number_of_node, edge_percentage, chance)
                random_generate_graph(number_of_node, edge_percentage, chance, folder + "/" + file_name)

gen_battery_test()