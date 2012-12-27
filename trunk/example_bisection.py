#!/usr/bin/python
# Ben Payne
# bpayne@lps.umd.edu
import networkx as nx
import matplotlib.pyplot as plt

connections_bbw1 = [[-1,1],[-2,1],[-3,1],[-4,1],[1,2],[2,3],[2,4],[2,5],[2,6],[3,-8],[4,-7],[5,-6],[6,-5]]
connections_bbw2 = [[-1,1],[-2,2],[-3,3],[-4,4],[1,4],[1,3],[2,4],[2,3]]
  
G1=nx.Graph()
G2=nx.Graph()

G1.add_edges_from(connections_bbw1)
G2.add_edges_from(connections_bbw2)

nx.draw(G1)
plt.show()

nx.draw(G2)
plt.show()

