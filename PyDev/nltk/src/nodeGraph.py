#coding: utf-8

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.font_manager as fm
import nltk

class myGraph(object):
    
    def __init__(self):
        self.G = nx.Graph()
        self.size = None
        prop = fm.FontProperties(fname='C:\WINDOWS\Fonts\msmincho.ttc')
        nx.set_fontproperties(prop)     #need patch: https://gist.github.com/1247256
                
    def setparameterFromList(self,list):
        pass
    
    def setparameterFromDict(self,dict):
        for k,vs in dict.iteritems():
            self.G.add_node(k) 
        self.size = [vs_ for vs_ in dict.itervalues()]
    
        
    def drawGraph(self):
        nx.draw(self.G,node_size=self.size)
        plt.show()
        pass
        

def graph_draw():
    G = nx.DiGraph()
    a = u'薬品∀'
    b = u'薬品Ｂ'
    c = u'薬品Ｘ'
    
    udict_ = nltk.defaultdict(int)
    udict_[a] = 1000
    udict_[b] = 2000
    udict_[c] = 30000    
    
    #myG =  myGraph()
    #myG.setparameterFromDict(udict_)
    #myG.drawGraph()
    G.add_edge(a, b)
    G.add_edge(c, b)
    #H = nx.path_graph(10)
    #G.add_nodes_from(H)
    nx.draw_circular(G)
    
    plt.show()
    
def main():
    graph_draw()
    
if __name__ == '__main__':
    main()

