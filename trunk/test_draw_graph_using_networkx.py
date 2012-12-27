import networkx as nx
import matplotlib.pyplot as plt
import lib_network_optimization as nopt

# http://networkx.lanl.gov/tutorial/tutorial.html

number_of_switches,number_of_computers,connections=nopt.readGraphFromFile()

G=nx.Graph()

G.add_edges_from(connections)

# The following colorization of nodes works but cannot be drawn
#for nodeIndx, nodeValue in enumerate(G.nodes()):
  #if (nodeValue<0):
    #G[nodeValue]['color']='red'
  #elif (nodeValue>0):
    #G[nodeValue]['color']='blue'
  #else:
    #print ("error in connections node value")
  

nx.draw(G)
plt.show()
plt.savefig("networkx_draw.png")

nx.draw_random(G)
plt.show()
plt.savefig("networkx_random.png")
nx.draw_circular(G)
plt.show()
plt.savefig("networkx_circular.png")
nx.draw_spectral(G)
plt.show()
plt.savefig("networkx_spectral.png")
