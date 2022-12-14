import osmnx as ox 
import networkx as nx
import matplotlib.pyplot as plt
import time 

def load_r(filename="../data/shanghai.xml", bbox=None):
    '''
    bbox: (min_lat, max_lat, min_longi, max_longi) # (north, south, east, west)
    '''
    G = ox.load_graphml(filename)
    print("edges: ", len(G.edges))
    print("nodes: ", len(G.nodes))
    if bbox:
        G = ox.truncate.truncate_graph_bbox(G, *bbox)
        print("edges: ", len(G.edges))
        print("nodes: ", len(G.nodes))        
    return G

def savefig(G:nx.MultiDiGraph):
    ox.plot_graph(G, node_size=8, save=True, filepath="shanghai.png", dpi=300)

def save_r(G, filename="../data/shanghai.xml"):
    ox.save_graphml(G, filename)

if __name__ == "__main__":
    begin_time = time.time()
    G = load_r()
    savefig(G)
    print("time used: ", time.time() - begin_time)

