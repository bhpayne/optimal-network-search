#!/usr/bin/python
import networkx as nx
import matplotlib.pyplot as plt

def color_graph_nodes(G,compute_color,router_color):
  all_nodes=G.nodes()
  node_color_list=[]
  for indx in range(len(all_nodes)):
    if (all_nodes[indx]<0):
      node_color_list.append(compute_color)
    elif (all_nodes[indx]>0):
      node_color_list.append(router_color)
    else:
      print("invalid node value")
      exit(1)
  return node_color_list

connections_bbw = [[-1,1],[-2,2],[-3,3],[-4,4],[1,4],[1,3],[2,4],[2,3]] # good
# connections_bbw = [[-1,1],[-2,1],[-3,1],[-4,1],[1,2],[2,3],[2,4],[2,5],[2,6],[3,-8],[4,-7],[5,-6],[6,-5]] # bad
G=nx.Graph()
G.add_edges_from(connections_bbw)
compute_color='red'
router_color='blue'
node_color_list=color_graph_nodes(G,compute_color,router_color)
nx.draw(G,node_color=node_color_list)
plt.show()
