#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: 

# output: 

import networkx as nx
import lib_network_optimization as nopt # Ben's module for graph input/output
import itertools           # for generating pairs of computers 

#************ MAIN BODY *********************

number_of_routers=5
number_of_ports_per_router=10
number_of_computers=10
number_of_ports_per_computer=1
number_of_iterations=1000 # how many evolutions to make
random_network_search_limit=1000 # used for random graph generation
valid_path_search_limit=100 
search_mod_alert=20 # how often to display that no path modification has been found
nopt.sanity_checks(number_of_routers,number_of_computers,number_of_ports_per_computer,number_of_ports_per_router)
connections = nopt.generate_random_network(number_of_computers,number_of_ports_per_computer,number_of_routers,number_of_ports_per_router,random_network_search_limit)
# alternatives to random graph:
# connections = nopt.generate_2D_mesh_network(number_of_rows,number_of_columns)
# and
# connections = nopt.generate_ND_toroidal_or_mesh_network(dimensions,toroidal_true_mesh_false)
# as an example,
# dimensions=[2,3,5]
# toroidal_true_mesh_false=True


nopt.draw_graph_pictures(connections,"initial")

found_valid_mutation=0 # false
search_indx=0
while ((not found_valid_mutation) and (search_indx<valid_path_search_limit)):
  try:
    hop_count_distribution=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections)
    average_hop_count=float(sum(hop_count_distribution))/len(hop_count_distribution)
    print ("initial average hop count is "+str(average_hop_count))
    #max_hop_count = max(hop_count_distribution)
    #print ("maximum hop count is "+str(max_hop_count))
    found_valid_mutation=1 # true 
    break
  except nx.NetworkXNoPath:
    if ((search_indx%search_mod_alert)==0):
      print('No path for this alteration, loop index='+str(search_indx))
    search_indx=search_indx+1

time_marker=0
while (time_marker<number_of_iterations):
  #print("reached while loop")
  connections_new=nopt.make_alteration_swap_ports(number_of_routers,number_of_computers,connections)
  #print connections_new
  #draw_graph_pictures(connections_new,"new")
  found_valid_mutation=0 # false
  search_indx=0
  while ((not found_valid_mutation) and (search_indx<valid_path_search_limit)):
    try:
      hop_count_distribution_new=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections_new)
      average_hop_count_new=float(sum(hop_count_distribution_new))/len(hop_count_distribution_new)
      #print ("new average hop count is "+str(average_hop_count_new))
      found_valid_mutation=1 # true 
      break
    except nx.NetworkXNoPath:
      if ((search_indx%search_mod_alert)==0):
        print('No path for this alteration, loop index='+str(search_indx))
      search_indx=search_indx+1

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
  
  