#coding: utf-8
import matplotlib.pyplot as plt
import networkx as nx
import numpy 

from collections import defaultdict
from scipy.cluster import hierarchy
from scipy.spatial import distance

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
prop = fm.FontProperties(fname='C:\WINDOWS\Fonts\msmincho.ttc')
nx.set_fontproperties(prop)     #need patch: https://gist.github.com/1247256

def normalizebarabasi():
    
    G = nx.barabasi_albert_graph(10, 3)
    degree_list_ = G.degree()
    pos = nx.spring_layout(G)

    for d_ in degree_list_.values():
        print "degree list:", d_
        
    for c_,v in nx.clustering(G).iteritems():
        print c_,v
        
    fig=plt.figure(1,figsize=(6,10))
    ax=fig.add_subplot(211)
    nx.draw_networkx_edges(G,pos,width=0.2)
    plt.show()

def create_hc(G):
    """Creates hierarchical cluster of graph G from distance matrix"""
    path_length=nx.all_pairs_shortest_path_length(G)
    distances=numpy.zeros((len(G),len(G)))
    for u,p in path_length.items():
        for v,d in p.items():
            distances[u][v]=d
    # Create hierarchical cluster
    Y=distance.squareform(distances)
    Z=hierarchy.complete(Y)  # Creates HC using farthest point linkage
    # This partition selection is arbitrary, for illustrive purposes
    membership=list(hierarchy.fcluster(Z,t=1.15))
    # Create collection of lists for blockmodel
    partition=defaultdict(list)
    for n,p in zip(list(range(len(G))),membership):
        partition[p].append(n)
    return list(partition.values())


def multnet():
    G=nx.MultiDiGraph()
    G=nx.read_edgelist("c:\\temp\\mdrug.csv")
    
    for n_ in G.nodes_iter():
        for m_ in G[n_]:
            print "tail:",n_,"head:",m_,"G[n][m]:",G[n_][m_]
    
    
    H=nx.connected_component_subgraphs(G)[0]
    H=nx.convert_node_labels_to_integers(H)

    for n_ in H.nodes_iter():
        for m_ in H[n_]:
            print "tail:",n_,"head:",m_,"H[n][m]:",H[n_][m_]


    
    fig=plt.figure(1,figsize=(6,10))
    ax=fig.add_subplot(211)
    nx.draw(G)
    ax=fig.add_subplot(212)
    nx.draw(H)
    
    plt.show()
    """
    partitions=create_hc(H)
    BM=nx.blockmodel(H,partitions)
    # Draw original graph
    pos=nx.spring_layout(H,iterations=100)
    fig=plt.figure(1,figsize=(6,10))
    ax=fig.add_subplot(211)
    nx.draw(H,pos,with_labels=False,node_size=10)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.show()
    """

def fileprocess():
    FILE = "c:\\temp\\mdrug.txt"    
    f = open(FILE,'rU')
    lines = f.readlines()
    rows = lines
    rowlength = len(lines)
    print rowlength
    
    lists_ = []
    for r_ in rows:
        rr = r_.split(',')
        data_ = (rr[0].decode('cp932'),rr[1].decode('cp932'))
        lists_.append(data_)
        
    G = nx.Graph()
    G.add_edges_from(lists_)
    degree_ =  G.degree()
    ds = sortedmap(degree_)
    for k_,v_ in ds[0:10]:
        print k_,v_
    
    sizes_ = []
    bignodes_ = []
    nodes_ = []    
    for idx,d_ in enumerate(degree_.values()):
        if d_ > 10:
            sizes_.append(d_ * 10)
            bignodes_.append(idx)
        else:
            sizes_.append(d_ * 5)
            nodes_.append(idx)
        #pos = nx.spring_layout(self.G)
    
    #pos = nx.spring_layout(G)
    #nx.draw_networkx_nodes(G, pos, node_color = 'r')
    #nx.draw_networkx_edges(G, pos, width = 1, alpha=0.3)
    #nx.draw_networkx_labels(G, pos, font_size = 12, font_family = 'msmincho', font_color = 'blue')
    
    h = plt.hist(degree_.values(),bins=100)
    plt.loglog(h[1][1:],h[0])
    
    
    plt.show()

def sortedmap(map):
    ms = sorted(map.iteritems(),key = lambda (k,v):(-v,k))
    return ms

def main():
    #normalizebarabasi()
    #multnet()
    fileprocess()
    
if __name__ == '__main__':
    main()