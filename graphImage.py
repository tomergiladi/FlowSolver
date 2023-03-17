import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def graphImage(G):
    
    #plot the nodes with color 
    for n in G.nodes:
        c= np.array([[0,0,0]]) if G.nodes[n]['color'] == -1 \
            else np.array([G.colors[G.nodes[n]['color']]])
        c=c/255
        c[0,0],c[0,2] = c[0,2],c[0,0]
        plt.scatter(n[1],n[0],c=c)
    #draw the edges with color
    for e in G.edges:
        if G.edges[e]['color'] == -1:
            continue
        c= np.array([G.colors[G.edges[e]['color']]])
        c=c/255
        c[0,0],c[0,2] = c[0,2],c[0,0]
        plt.plot([e[0][1],e[1][1]],[e[0][0],e[1][0]],c=c)

    


    
