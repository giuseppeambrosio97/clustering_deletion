import networkx as nx

def check_solution(G: nx.Graph, G_sol: nx.Graph, val: int) -> bool:

    cliques = []
    n_nodes = 0

    for node in G_sol.nodes:
        clique = G_sol.nodes[node]["clique"]
        n_nodes += len(clique)
        cliques.append(clique)

    if n_nodes != len(G.nodes):
        return "Il numero dei nodi non coincide"

    def isClique(G, clique):
        for i in range(len(clique)):
            for j in range(i+1, len(clique)):
                if not G.has_edge(clique[i], clique[j]):
                    return False
                else:
                    G.remove_edge(clique[i], clique[j])
        return True

    for clique in cliques:
        if not isClique(G, list(clique)):
            return "L'insieme di vertici {} non è una clique nel grafo di input".format(clique)
    if val == len(G.edges):
        return True
    else:
        return "val = {} ed è diverso dal numero di edge rimanenti {} se eliminate le clique ".format(val, len(G.edges))
