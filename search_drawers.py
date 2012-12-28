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


def done_searching(metric_initial,metric_best,connections_best,tracker,metric_name_file,metric_name_label,t_start):
  print("initial: "+str(metric_initial)+", final best: "+str(metric_best))
  stream=file('network_connections_final.log','w')
  yaml.dump({'connections':connections},stream)
  stream.close()
  nopt.draw_drawer_graph_pictures(connections_best,"final")  
  plt.xlabel('iteration')
  plt.ylabel(metric_name_label)
  plt.plot(range(len(tracker)),tracker)  
  #plt.show()
  plt.savefig("networkx_"+metric_name_file+"_versus_iterations.png")
  plt.close()
  print("Total elapsed time: "+str(time.clock()-t_start)+" seconds")
  exit()

def how_many_picks(confidence,number_of_drawers,max_picks):
  #number of picks p = \frac{\log(1-c)}{\log(1-(1/U))}
  #where U = M! \prod_{x=0}^{N/2}(N-x)
  if ((number_of_drawers%2)==0):
    total_number = math.pow(2,(number_of_drawers/2))
  else:
    total_number = math.pow(2,((number_of_drawers+1)/2))
  if (math.log(1.0-(1.0/(total_number+0.0)))==0):
    print("warning: total number of permutations "+str(total_number)+" is too large for search (limited by float).")
    print("Setting number of picks = "+str(max_picks))
    # total_number is almost always too large for realistic networks to find bisection minimum with any confidence level
    number_of_picks=max_picks
  else:
    number_of_picks=int(math.ceil(math.log(1.0-((confidence+0.0)/100.0))/math.log(1.0-(1.0/(total_number+0.0)))))
  if (number_of_picks>max_picks):
    number_of_picks=max_picks
  print ("number of picks is "+str(number_of_picks))
  return number_of_picks
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

found_valid_initial_graph=False
search_indx=0
while ((not found_valid_initial_graph) and (search_indx<random_network_search_limit)):

  if (not specify_connections_input):
    connections = nopt.generate_random_drawer_network(number_of_drawers,number_of_ports_per_drawer,random_network_search_limit)
  
  try:
    hop_count_distribution=nopt.fitness_function_find_all_drawer_hop_lengths(number_of_drawers,connections)
    found_valid_initial_graph=True
    break
  except nx.NetworkXNoPath:
    print("initial network is segmented. Fix the random network generation algorithm")
    found_valid_initial_graph=False

t_found_initial_graph=time.clock()-t_read_input
print("time to find initial network: "+str(t_found_initial_graph)+" seconds")
# if you reach here, then the initial graph has been found to be valid
connections_best=connections
stream=file('network_connections_initial.log','w')
yaml.dump({'connections':connections},stream)
stream.close()

nopt.draw_drawer_graph_pictures(connections_best,"initial")

tracker=[]
if (use_hop_count):
  metric_name_file="average_hop_count"
  metric_name_label="average hop count"
  metric_best=float(sum(hop_count_distribution))/len(hop_count_distribution) # average hop count
  metric_initial=metric_best
  print ("initial "+metric_name_label+" is "+str(metric_best))
  tracker.append(metric_initial)
else:
  metric_name_file="minimum_bisection_count"
  metric_name_label="minimum bisection count"
  number_of_picks=how_many_picks(confidence_of_finding_minimum_bisection,number_of_drawers,max_picks)
  bisection_array=[]
  for bcount in range(number_of_picks):
    bisection_count=nopt.fitness_function_bisection_count_drawers(number_of_drawers,connections)
    bisection_array.append(bisection_count)
  metric_best=min(bisection_array)
  metric_initial=min(bisection_array)

temperature_indx=0
while (temperature_indx<number_of_iterations):
  t_find_altered_graph_previous=time.clock()
  found_valid_mutation=False
  search_indx=0
  while ((not found_valid_mutation) and (search_indx<valid_path_search_limit)):
    # simulated annealing: the number of mutations depends on the temperature
    if (use_simulated_annealing):
      for alteration_indx in range(random.randint(1,max_number_of_swaps*(1-(temperature_indx/number_of_iterations)))):
        connections_new=nopt.make_alteration_swap_ports_drawers(number_of_drawers,connections,random_network_search_limit)
    else:
      connections_new=nopt.make_alteration_swap_ports_drawers(number_of_drawers,connections,random_network_search_limit)
    try:
      hop_count_distribution_new=nopt.fitness_function_find_all_drawer_hop_lengths(number_of_drawers,connections_new)
      found_valid_mutation=True
      break
    except LookupError:
      #nopt.draw_drawer_graph_pictures(connections_new,"this failed")
      #print("failed")
      #exit()
      #if ((search_indx%search_mod_alert)==0):
        #print('This alteration segements the network. loop index='+str(search_indx))
      search_indx=search_indx+1
  if (search_indx==valid_path_search_limit):
    #print("reached valid_path_search_limit. Exiting")
    done_searching(metric_initial,metric_best,connections_best,tracker,metric_name_file,metric_name_label,t_start)

  t_find_altered_graph_new=time.clock()-t_find_altered_graph_previous
  #print("time to find altered network: "+str(t_find_altered_graph_new)+" seconds")
  
  t_metric_start=time.clock()
  if (use_hop_count):
    metric_new=float(sum(hop_count_distribution_new))/len(hop_count_distribution_new)
  else: # bisection
    bisection_array=[]
    for bcount in range(number_of_picks):
      bisection_count=nopt.fitness_function_bisection_count_drawers(number_of_drawers,connections)
      bisection_array.append(bisection_count)
    metric_new=min(bisection_array)
  tracker.append(metric_new)
  if (metric_new<metric_best):
    #print("improvement found")
    print("new best "+metric_name_label+" is "+str(metric_new)+" and old was "+str(metric_best))
    print("Total elapsed time: "+str(time.clock()-t_start)+" seconds")
    metric_best=metric_new
    connections_best=connections_new
    connections=connections_new
  temperature_indx=temperature_indx+1
  t_metric_elapsed=time.clock()-t_metric_start
  #print("time to determine metric: "+str(t_metric_elapsed)+" seconds. Total elapsed time: "+str(time.clock()-t_start)+" seconds")
  
done_searching(metric_initial,metric_best,connections_best,tracker,metric_name_file,metric_name_label,t_start)
