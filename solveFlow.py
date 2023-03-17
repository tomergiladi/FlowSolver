import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from graphImage import graphImage
import heapq


def heuristic(g,terminals):
    # return the sum of distances between each pair of terminals

    #get the shortest path between each pair of terminals
    sum=0
    for t1,t2 in terminals:
        try:
            sum += nx.shortest_path_length(g,t1,t2)
        except:
            sum+=100000
    g.add_node(0)
    for t1,t2 in terminals:
        g.add_edge(0,t1)
    
    lengths,path = nx.single_source_dijkstra(g,0)
    
    sum+=0 if len(lengths) == len(g.nodes) else 100000
    g.remove_node(0)

    return sum


#load graph from file
G = nx.read_gpickle("data/flow-8mania-2/sol.gpickle")

#remove all edges attributes
for e in G.edges:
    G.edges[e]['color'] = -1
#freeze the graph
#remove incoming edges from nodes that are terminals
for t1,t2 in G.terminals:
    G.remove_edges_from(list(G.in_edges(t1)))
    G.remove_edges_from(list(G.out_edges(t2)))

G = nx.freeze(G)

open = {(tuple(G.nodes),tuple(G.edges),G.terminals):G}
#create a priority queue
queue = []
heapq.heappush(queue,(0,next(iter(open.keys()))))
closed =set()
while queue:
    #get the graph with the lowest cost
    cost,key = heapq.heappop(queue)
    nodes,edges,terminals = key
    closed.add( key)
    sol=open.pop(key)
    # graphImage(sol)
    # plt.title("cost: "+str(cost))
    # plt.show(block=False)
    # plt.pause(0.1)
    # plt.clf()
    print(len(closed),cost)
    if len(terminals) == 0:
        print("found solution")
        graphImage(sol)
        plt.title("cost: "+str(cost))
        plt.show(block=False)
        plt.pause(3)
        break
    g= nx.DiGraph(edges)
    g.add_nodes_from(nodes)

    for i,(t1,t2) in enumerate(terminals):
        for k in g.neighbors(t1):

            gnew = nx.DiGraph(g)
            solnew= sol.copy()
            solnew.colors=G.colors
            gnew.remove_node(t1)

            if k != t2:
                terminalsnew = terminals[:i]+((k,t2),)+terminals[i+1:]
                gnew.remove_edges_from(list(gnew.in_edges(k)))
            else:
                terminalsnew = terminals[:i]+terminals[i+1:]
                gnew.remove_node(t2)
                

            key = (frozenset(gnew.nodes),frozenset(gnew.edges),terminalsnew)
            if key in closed or key in open:
                continue 

            
            solnew.edges[t1,k]['color'] = sol.nodes[t1]['color']
            solnew.nodes[k]['color'] = sol.nodes[t1]['color']
            

            open[key]=solnew
            h = heuristic(gnew,terminalsnew)
            heapq.heappush(queue,(h,key))
            
        

print(len(closed))  


