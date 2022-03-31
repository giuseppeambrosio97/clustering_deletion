import networkx as nx

def readGraph_n_m(filepath:str) -> nx.Graph:
    file = open(filepath,"r")
    with open(filepath) as fp:
        line = fp.readline()
        a = line.split(" ")
        vertex =  int(a[2])
        toR = nx.Graph()
        for el in range(0,vertex):
            toR.add_node(int(el))
        #print("nodes", toR.nodes)
        while line:
            line = fp.readline()
            if(not line):
                break
            b = line.split("\n")[0].split(" ")
            toR.add_edge(int(b[0]),int(b[1]))
    file.close()
    return toR

def readGraph_m(filepath:str) -> nx.Graph:
    file = open(filepath,"r")
    with open(filepath) as fp:
        line = fp.readline() # salta la prima riga
        toR = nx.Graph()
        while line:
            line = fp.readline()
            if(not line):
                break
            b = line.split("\n")[0].split(" ")
            # if toR.has_edge(int(b[0]),int(b[1])):
            #    input("Arco già presente: {},{}".format(int(b[0]),int(b[1])))
            toR.add_edge(int(b[0]),int(b[1]))
    file.close()
    return toR

def readGraph_comma(filepath:str) -> nx.Graph:
    file = open(filepath,"r")
    with open(filepath) as fp:
        line = fp.readline()
        toR = nx.Graph()
        while line:
            line = fp.readline()
            if(not line):
                break
            b = line.split("\n")[0].split(",")
            # if toR.has_edge(int(b[0]),int(b[1])):
            #    input("Arco già presente: {},{}".format(int(b[0]),int(b[1])))
            toR.add_edge(int(b[0]),int(b[1]))
    file.close()
    return toR
