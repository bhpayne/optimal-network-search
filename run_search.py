#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: 

# output: 

import networkx as nx
import lib_network_optimization as nopt # Ben's module for graph input/output
import itertools           # for generating pairs of computers 
import matplotlib.pyplot as plt
import random

#************ MAIN BODY *********************

number_of_routers=5
number_of_ports_per_router=10
number_of_computers=30
number_of_ports_per_computer=1
number_of_iterations=100 # how many evolutions to make. Must be a positive integer
max_number_of_swaps=10
random_network_search_limit=1000 # used for random graph generation. Must be a positive integer
valid_path_search_limit=100 # Must be a positive integer
search_mod_alert=20 # how often to display that no path modification has been found. Must be a positive integer
nopt.sanity_checks(number_of_routers,number_of_computers,number_of_ports_per_computer,number_of_ports_per_router)

found_valid_initial_graph=False
search_indx=0
while ((not found_valid_initial_graph) and (search_indx<random_network_search_limit)):
  connections = nopt.generate_random_network(number_of_computers,number_of_ports_per_computer,number_of_routers,number_of_ports_per_router,random_network_search_limit)
  #alternatives to random graph:
  #connections = nopt.generate_2D_mesh_network(number_of_rows,number_of_columns)
  #and
  #connections = nopt.generate_ND_toroidal_or_mesh_network(dimensions,toroidal_true_mesh_false)
  #as an example,
  #dimensions=[2,3,5]
  #toroidal_true_mesh_false=True
  try:
    hop_count_distribution=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections)
    found_valid_initial_graph=True
    break
  except nx.NetworkXNoPath:
    print("initial network is segmented. Fix the random network generation algorithm")
    found_valid_initial_graph=False

# if you reach here, then the initial graph has been found to be valid
connections_best=connections
nopt.draw_graph_pictures(connections_best,"initial")

average_hop_count_best=float(sum(hop_count_distribution))/len(hop_count_distribution)
average_hop_count_initial=average_hop_count_best
print ("initial average hop count is "+str(average_hop_count_best))
tracker=[]
tracker.append(average_hop_count_initial)

time_marker=0
while (time_marker<number_of_iterations):
  #print("reached while loop")
  found_valid_mutation=False
  search_indx=0
  while ((not found_valid_mutation) and (search_indx<valid_path_search_limit)):
    for alteration_indx in range(random.randint(1,max_number_of_swaps)):
      connections_new=nopt.make_alteration_swap_ports(number_of_routers,number_of_computers,connections,random_network_search_limit)
    try:
      hop_count_distribution_new=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections_new)
      found_valid_mutation=True
      break
    except nx.NetworkXNoPath:
      #nopt.draw_graph_pictures(connections_new,"this failed")
      #print("failed")
      #exit()
      if ((search_indx%search_mod_alert)==0):
        print('This alteration segements the network. loop index='+str(search_indx))
      search_indx=search_indx+1
  if (search_indx==valid_path_search_limit):
    print("reached valid_path_search_limit. Exiting")
    exit()
    
  average_hop_count_new=float(sum(hop_count_distribution_new))/len(hop_count_distribution_new)
  if (average_hop_count_new<average_hop_count_best):
    #print("improvement found")
    print ("new best average hop count is "+str(average_hop_count_new)+" and old was "+str(average_hop_count_best))
    average_hop_count_best=average_hop_count_new
    connections_best=connections_new
    connections=connections_new
  else:
    print ("new average hop count is "+str(average_hop_count_new)+" and best remains "+str(average_hop_count_best))
    tracker.append(average_hop_count_new)
  time_marker=time_marker+1

print("initial: "+str(average_hop_count_initial)+", final best: "+str(average_hop_count_best))
nopt.draw_graph_pictures(connections,"final")  
plt.xlabel('iteration')
plt.ylabel('average hop count')
plt.plot(range(len(tracker)),tracker)  
plt.show()