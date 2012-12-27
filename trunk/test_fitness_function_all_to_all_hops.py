#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: measure the number of hops between all pairs of compute nodes

# output: 

import networkx as nx
import matplotlib.pyplot as plt
import networkgraphio as ngio # Ben's module for graph input/output
import itertools           # for generating pairs of computers 
import lib_fitness_function_all_to_all_hops

# http://networkx.lanl.gov/reference/generated/networkx.algorithms.shortest_paths.unweighted.all_pairs_shortest_path.html#networkx.algorithms.shortest_paths.unweighted.all_pairs_shortest_path

# http://networkx.lanl.gov/reference/generated/networkx.algorithms.simple_paths.all_simple_paths.html#networkx.algorithms.simple_paths.all_simple_paths
# http://networkx.lanl.gov/reference/algorithms.shortest_paths.html#module-networkx.algorithms.shortest_paths.unweighted

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
all_lengths=lib_fitness_function_all_to_all_hops.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections)
  
average_hop_count = float(sum(all_lengths)) / len(all_lengths)
print ("average hop count is "+str(average_hop_count))
max_hop_count = max(all_lengths)
print ("maximum hop count is "+str(max_hop_count))
