#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: 

# output: 

import networkx as nx
import matplotlib.pyplot as plt
import networkgraphio as ngio # Ben's module for graph input/output
import itertools           # for generating pairs of computers 

G = generate_random_network(number_of_computers,number_of_ports_per_computer,number_of_routers,number_of_ports_per_router)

Gbest=G

hop_count_distribution=fitness_function_hop_count(G)
average_hop_count=sum(hop_count_distribution)/len(hop_count_distribution)

time_marker=0
while (time_marker<100):
  Gnew = modify_graph(G)

  hop_count_distribution_new=fitness_function_hop_count(Gnew)
  average_hop_count_new=sum(hop_count_distribution_new)/len(hop_count_distribution_new)

  if (average_hop_count_new<average_hop_count):
    Gbest=Gnew
    