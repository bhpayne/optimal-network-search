#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: 

# output: 

import networkx as nx
import matplotlib.pyplot as plt
import lib_network_optimization as nopt # Ben's module for graph input/output
import itertools           # for generating pairs of computers 

#************ MAIN BODY *********************

number_of_routers=10
number_of_ports_per_router=10
number_of_computers=10
number_of_ports_per_computer=1
number_of_iterations=1000
search_loop_limit=1000 # used for random graph generation

connections = nopt.generate_random_network(number_of_computers,number_of_ports_per_computer,number_of_routers,number_of_ports_per_router,search_loop_limit)

nopt.draw_graph_pictures(connections,"initial")

hop_count_distribution=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections)
average_hop_count=float(sum(hop_count_distribution))/len(hop_count_distribution)
print ("initial average hop count is "+str(average_hop_count))
#max_hop_count = max(hop_count_distribution)
#print ("maximum hop count is "+str(max_hop_count))

time_marker=0
while (time_marker<number_of_iterations):
  #print("reached while loop")
  connections_new=nopt.make_alteration_swap_ports(number_of_routers,number_of_computers,connections)
  #print connections_new
  #draw_graph_pictures(connections_new,"new")
  hop_count_distribution_new=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections_new)
  average_hop_count_new=float(sum(hop_count_distribution_new))/len(hop_count_distribution_new)
  #print ("new average hop count is "+str(average_hop_count_new))

  if (average_hop_count_new<average_hop_count):
    #print("improvement found")
    print ("new average hop count is "+str(average_hop_count_new))
    connections_best=connections_new
    connections=connections_new
    average_hop_count=average_hop_count_new
  #else:
    #print("new network is not better than previous")
  time_marker=time_marker+1
  
nopt.draw_graph_pictures(connections,"final")  
  
  