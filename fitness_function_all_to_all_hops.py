#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: measure the number of hops between all pairs of compute nodes

# output: 

import networkx as nx
import matplotlib.pyplot as plt
import networkgraphio as ngio # Ben's module for graph input/output
import itertools           # for generating pairs of computers 

# http://networkx.lanl.gov/reference/generated/networkx.algorithms.shortest_paths.unweighted.all_pairs_shortest_path.html#networkx.algorithms.shortest_paths.unweighted.all_pairs_shortest_path

# http://networkx.lanl.gov/reference/generated/networkx.algorithms.simple_paths.all_simple_paths.html#networkx.algorithms.simple_paths.all_simple_paths
# http://networkx.lanl.gov/reference/algorithms.shortest_paths.html#module-networkx.algorithms.shortest_paths.unweighted

def find_all_compute_hop_lengths(number_of_computers,G):
  all_pairs=list(itertools.combinations(range(1,number_of_computers+1), 2))

  # http://networkx.lanl.gov/reference/generated/networkx.algorithms.shortest_paths.generic.shortest_path_length.html#networkx.algorithms.shortest_paths.generic.shortest_path_length
  all_lengths=[]
  for pair_indx in range(len(all_pairs)):
    computerA=all_pairs[pair_indx][0]*-1
    computerB=all_pairs[pair_indx][1]*-1
    length_between_compute_nodes=nx.shortest_path_length(G,source=computerA,target=computerB)
    #print length_compute_nodes
    all_lengths.append(length_between_compute_nodes)
  return all_lengths
    
number_of_switches,number_of_computers,connections=ngio.readGraphFromFile()

G=nx.Graph()

G.add_edges_from(connections)

## http://networkx.lanl.gov/reference/generated/networkx.algorithms.shortest_paths.dense.floyd_warshall.html#networkx.algorithms.shortest_paths.dense.floyd_warshall
#distnc=nx.floyd_warshall(G) # dictionary of all pair distances
## now distnc.keys() == connections
## the distance between any to nodes A, B is given by distnc[A][B]
## as expected, distnc[A][A]==0
## and an edge=1 unit of distance

# alternative:
# path=nx.all_pairs_shortest_path(G)

#>>> len(list(itertools.combinations(range(1000), 2)))
#     499,500
all_lengths=find_all_compute_hop_lengths(number_of_computers,G)
  
average_hop_count = float(sum(all_lengths)) / len(all_lengths)
print ("average hop count is "+str(average_hop_count))
max_hop_count = max(all_lengths)
print ("maximum hop count is "+str(max_hop_count))
