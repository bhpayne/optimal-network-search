#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: 

# to do:
# add and implement the following booleans:
# allow_redundant_connections_between_routers=True

# usage:
# python run_search.py

# with profiling:
# http://stackoverflow.com/questions/582336/how-can-you-profile-a-python-script

# python -m cProfile -s time -o profile_result.log run_search.py

# sudo easy_install pycallgraph
# pycallgraph run_search.py
# eog pycallgraph.png

# pycallgraph -f svg -o pycallgraph.svg run_search.py

# output: 

import networkx as nx
import lib_network_optimization as nopt # Ben's module for graph input/output
import matplotlib.pyplot as plt
import random
import math
import yaml
import time


#************ MAIN BODY *********************

t_start = time.clock()

input_stream=file('parameters_drawers.input','r')
input_data=yaml.load(input_stream)

confidence_of_finding_minimum_bisection=input_data["confidence"]
max_picks=input_data["max_picks"]
search_mod_alert=input_data["search_mod_alert"]
number_of_iterations=input_data["number_of_iterations"]
random_network_search_limit=input_data["random_network_search_limit"]
valid_path_search_limit=input_data["valid_path_search_limit"]
max_number_of_swaps=input_data["max_number_of_swaps"]
specify_connections_input=input_data["specify_connections_input"]
connections=input_data["connections"]
use_hop_count=input_data["use_hop_count"]
use_simulated_annealing=input_data["use_simulated_annealing"]

number_of_drawers=input_data["number_of_drawers"]
number_of_ports_per_drawer=input_data["number_of_ports_per_drawer"]

input_stream.close()

t_read_input = time.clock() - t_start # CPU seconds elapsed 
#print("time to read input: "+str(t_read_input)+" seconds")

print("number of drawers:            "+str(number_of_drawers))
print("number of ports per drawer:   "+str(number_of_ports_per_drawer))
if (use_hop_count):
  print("metric: hop count")
else:
  print("metric: bisection count")
if (use_simulated_annealing):
  print("using simulated annealing")
else:
  print("NOT using simulated annealing")
  
found_valid_initial_graph=False
search_indx=0
while ((not found_valid_initial_graph) and (search_indx<random_network_search_limit)):

  if (not specify_connections_input):
    connections = nopt.generate_random_drawer_network(number_of_drawers,number_of_ports_per_drawer,random_network_search_limit)

  # need to determine whether the graph is segmented. Test: can each node reach all other nodes?
  try:
    hop_count_distribution=nopt.fitness_function_find_all_drawer_hop_lengths(number_of_drawers,connections)
    found_valid_initial_graph=True
    break
  except KeyError: # the referenced key doesn't exist in the dictionary. This indicates there is no path between two nodes
    print("initial network is segmented. Fix the random network generation algorithm")
    found_valid_initial_graph=False

t_found_initial_graph=time.clock()-t_read_input
print("time to find initial network: "+str(t_found_initial_graph)+" seconds")
# if you reach here, then the initial graph has been found to be valid
connections_best=connections
connections_prev=connections
stream=file('network_connections_initial.log','w')
yaml.dump({'connections':connections},stream)
stream.close()

nopt.draw_drawer_graph_pictures(connections_best,"initial")

tracker_all=[]
tracker_mins=[]
tracker_mins_indx=[]
if (use_hop_count):
  metric_name_file="average_hop_count"
  metric_name_label="average hop count"
  metric_initial=float(sum(hop_count_distribution))/len(hop_count_distribution) # average hop count
  metric_best=metric_initial
else:
  metric_name_file="minimum_bisection_count"
  metric_name_label="minimum bisection count"
  number_of_picks=how_many_picks_drawers(confidence_of_finding_minimum_bisection,number_of_drawers,max_picks)
  bisection_array=[]
  for bcount in range(number_of_picks):
    bisection_count=nopt.fitness_function_bisection_count_drawers(number_of_drawers,connections)
    bisection_array.append(bisection_count)
  metric_initial=min(bisection_array)
  metric_best=metric_initial

print ("initial "+metric_name_label+" is "+str(metric_best))
tracker_all.append(metric_initial)
tracker_mins.append(metric_initial)
tracker_mins_indx.append(0)
  
for temperature_indx in range(1,number_of_iterations+1):
  t_find_altered_graph_previous=time.clock()
  found_valid_mutation=False
  search_indx=0
  while ((not found_valid_mutation) and (search_indx<valid_path_search_limit)):
    #nopt.draw_drawer_graph_pictures(connections,"prior_to_mutation")
    #print("connections prior to mutation:")
    #print connections
    if (use_simulated_annealing):   # simulated annealing: the number of mutations depends on the temperature
      upper_limit=max([1,max_number_of_swaps*(1.0-(temperature_indx/number_of_iterations))])
      #print('max swaps: '+str(max_swap))
      number_of_swaps=random.randint(1,upper_limit)
      #print('number of swaps: '+str(number_of_swaps))
      for alteration_indx in range(number_of_swaps): # perform a random number of swaps
        connections_new=nopt.make_alteration_swap_ports_drawers(number_of_drawers,connections,random_network_search_limit)
    else: # only perform one swap. Useful for troubleshooting
      connections_new=nopt.make_alteration_swap_ports_drawers(number_of_drawers,connections,random_network_search_limit)
    try:
      hop_count_distribution_new=nopt.fitness_function_find_all_drawer_hop_lengths(number_of_drawers,connections_new)
      found_valid_mutation=True
      break
    except KeyError: # the referenced key doesn't exist in the dictionary. This indicates there is no path between two nodes
      found_valid_mutation=False
      nopt.draw_drawer_graph_pictures(connections_new,"this_failed")
      print("mutation caused network segmentation")
      print("connections after mutation:")
      print connections
      exit()
      #if ((search_indx%search_mod_alert)==0):
        #print('This alteration segements the network. loop index='+str(search_indx))
      search_indx=search_indx+1
  # here the while loop has terminated either due to finding a valid mutation or reaching valid_path_search_limit
  if (search_indx==valid_path_search_limit):
    print("reached valid_path_search_limit. Exiting")
    nopt.done_searching(metric_initial,metric_best,connections_best,tracker_all,tracker_mins,tracker_mins_indx,metric_name_file,metric_name_label,t_start)
    nopt.draw_drawer_graph_pictures(connections,"final")  
  t_find_altered_graph_new=time.clock()-t_find_altered_graph_previous
  #print("time to find altered network: "+str(t_find_altered_graph_new)+" seconds")
  
  t_metric_start=time.clock()
  if (use_hop_count):
    metric_new=float(sum(hop_count_distribution_new))/len(hop_count_distribution_new)
    this_change_is_an_improvement = (metric_new<metric_best)
  else: # bisection
    bisection_array=[]
    for bcount in range(number_of_picks):
      bisection_count=nopt.fitness_function_bisection_count_drawers(number_of_drawers,connections)
      bisection_array.append(bisection_count)
    metric_new=min(bisection_array)
    this_change_is_an_improvement = (metric_new<metric_best)
  tracker_all.append(metric_new)
  #print(temperature_indx)
  if (this_change_is_an_improvement):
    #print("improvement found at temperature index "+str(temperature_indx))
    tracker_mins.append(metric_new)
    tracker_mins_indx.append(temperature_indx)
    print("new best "+metric_name_label+" is "+str(metric_new)+" at temp index "+str(temperature_indx)+" and old was "+str(metric_best))
    print("Total elapsed time: "+str(time.clock()-t_start)+" seconds")
    metric_best=metric_new
    connections_best=connections_new
    connections=connections_new
    connections_prev=connections_new
  else:
    connections=connections_prev
  t_metric_elapsed=time.clock()-t_metric_start
  #print("time to determine metric: "+str(t_metric_elapsed)+" seconds. Total elapsed time: "+str(time.clock()-t_start)+" seconds")
  
nopt.done_searching(metric_initial,metric_best,connections_best,tracker_all,tracker_mins,tracker_mins_indx,metric_name_file,metric_name_label,t_start)
nopt.draw_drawer_graph_pictures(connections,"final")  
print("Total elapsed time: "+str(time.clock()-t_start)+" seconds")
