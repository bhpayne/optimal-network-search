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
#import matplotlib.pyplot as plt
import random
import math
import yaml
import time


#************ MAIN BODY *********************

t_start = time.clock()

input_stream=file('parameters_computers_and_routers.input','r')
input_data=yaml.load(input_stream)

# real-valued scalar
confidence_of_finding_minimum_bisection=input_data["confidence"]
max_picks=input_data["max_picks"]
search_mod_alert=input_data["search_mod_alert"]
min_temp=input_data["min_temp"]
max_number_of_iterations=input_data["max_number_of_iterations"]
random_network_search_limit=input_data["random_network_search_limit"]
valid_path_search_limit=input_data["valid_path_search_limit"]
max_number_of_swaps=input_data["max_number_of_swaps"]
initial_temperature_value=input_data["temperature_value"]
cooling_rate=input_data["cooling_rate"]
number_of_searches=input_data["number_of_searches"]

# booleans:
specify_connections_input=input_data["specify_connections_input"]
use_hop_count=input_data["use_hop_count"]
use_bisection_count=input_data["use_bisection_count"]
use_timeToSolution=input_data["use_timeToSolution"]
use_simulated_annealing=input_data["use_simulated_annealing"]

# array
connections=input_data["connections"] # may be needed if specify_connections_input==True

number_of_computers=input_data["number_of_computers"]
number_of_ports_per_computer=input_data["number_of_ports_per_computer"]
number_of_routers=input_data["number_of_routers"]
number_of_ports_per_router=input_data["number_of_ports_per_router"]

input_stream.close() # done reading parameters input

nopt.sanity_checks(number_of_routers,number_of_computers,number_of_ports_per_computer,number_of_ports_per_router)

metric_best_of_all=10000000
connections_best_of_all=[]

all_search_results=[]
for this_search_indx in range(number_of_searches):
  print this_search_indx
  temperature_value=initial_temperature_value
  t_read_input = time.clock() - t_start # CPU seconds elapsed 
  #print("time to read input: "+str(t_read_input)+" seconds")

  if (not specify_connections_input):
    print("number of computers:          "+str(number_of_computers))
    print("number of ports per computer: "+str(number_of_ports_per_computer))
    print("number of routers:            "+str(number_of_routers))
    print("number of ports per router:   "+str(number_of_ports_per_router))
  if (use_hop_count):
    print("metric: hop count")
  if (use_bisection_count):
    print("metric: bisection count")
  if (use_timeToSolution):
    print("metric: time to solution")
  if (use_simulated_annealing):
    print("using simulated annealing")
  else:
    print("NOT using simulated annealing")
    
  found_valid_initial_graph=False
  search_indx=0
  while ((not found_valid_initial_graph) and (search_indx<random_network_search_limit)):

    if (not specify_connections_input):
      connections = nopt.generate_random_computer_and_router_network(number_of_computers,number_of_ports_per_computer,number_of_routers,number_of_ports_per_router,random_network_search_limit)
    else:    #alternatives to random graph
      number_of_rows=4
      number_of_columns=4
      connections = nopt.generate_2D_mesh_network(number_of_rows,number_of_columns)
      number_of_computers=number_of_rows*number_of_columns
      number_of_routers=number_of_rows*number_of_columns
      number_of_ports_per_computer=1
      number_of_ports_per_router=5
      #dimensions=[2,3,5]
      #toroidal_true_mesh_false=True
      #connections = nopt.generate_ND_toroidal_or_mesh_network(dimensions,toroidal_true_mesh_false)
      #print connections

    try:
      hop_count_distribution=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections)
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

  nopt.draw_computer_and_router_graph_pictures(connections_best,"initial")

  tracker_all=[]
  tracker_mins=[]
  tracker_mins_indx=[]
  if (use_hop_count and not (use_bisection_count or use_timeToSolution)):
    metric_name_file="average_hop_count"
    metric_name_label="average hop count"
    metric_best=float(sum(hop_count_distribution))/len(hop_count_distribution) # average hop count
    metric_initial=metric_best
  elif (use_timeToSolution and not (use_hop_count or use_bisection_count)):
    metric_name_file="average_time_to_solution"
    metric_name_label="average time to solution"
    metric_best=nopt.fitness_function_average_time_to_solution(connections)
    metric_initial=metric_best    
  elif (use_bisection_count and not (use_hop_count or use_timeToSolution)):
    metric_name_file="minimum_bisection_count"
    metric_name_label="minimum bisection count"
    number_of_picks=nopt.how_many_picks_computers_routers(confidence_of_finding_minimum_bisection,number_of_computers,number_of_routers,max_picks)
    bisection_array=[]
    for bcount in range(number_of_picks):
      bisection_count=nopt.fitness_function_bisection_count_computers_and_routers(number_of_computers,number_of_routers,connections)
      bisection_array.append(bisection_count)
    metric_best=min(bisection_array)
    metric_initial=min(bisection_array)
  print ("initial "+metric_name_label+" is "+str(metric_best))
  tracker_all.append(metric_initial)
  tracker_mins.append(metric_initial)
  tracker_mins_indx.append(0)

  temperature_indx=0
  while (temperature_indx<max_number_of_iterations):
    t_find_altered_graph_previous=time.clock()
    found_valid_mutation=False
    search_indx=0
    while ((not found_valid_mutation) and (search_indx<valid_path_search_limit)):
      #if (use_simulated_annealing):
	#for alteration_indx in range(random.randint(1,max_number_of_swaps*(1-(temperature_indx/number_of_iterations)))):
      connections_new=nopt.make_alteration_swap_ports_routers_and_computers(number_of_routers,number_of_computers,connections,random_network_search_limit)
      #connections_new=nopt.make_alteration_add_or_remove_router(number_of_routers,number_of_computers,connections,random_network_search_limit)
	#connections_new=nopt.make_alteration_add_router_router_edge(number_of_routers,connections_new,number_of_ports_per_router,random_network_search_limit)
      #else:
	#connections_new=nopt.make_alteration_swap_ports_routers_and_computers(number_of_routers,number_of_computers,connections,random_network_search_limit)
      try:
	hop_count_distribution_new=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections_new)
	found_valid_mutation=True
	break
      except nx.NetworkXNoPath:
	#nopt.draw_computer_and_router_graph_pictures(connections_new,"this failed")
	#print("failed")
	#exit()
	#if ((search_indx%search_mod_alert)==0):
	  #print('This alteration segements the network. loop index='+str(search_indx))
	search_indx=search_indx+1
    if (search_indx==valid_path_search_limit):
      print("reached valid_path_search_limit="+str(valid_path_search_limit)+", but no valid networks were found through mutation. Exiting")
      nopt.done_searching(metric_initial,metric_best,connections_best,tracker_all,tracker_mins,tracker_mins_indx,metric_name_file,metric_name_label,t_start)
      nopt.draw_computer_and_router_graph_pictures(connections,"final")  

    t_find_altered_graph_new=time.clock()-t_find_altered_graph_previous
    #print("time to find altered network: "+str(t_find_altered_graph_new)+" seconds")
    
    t_metric_start=time.clock()
    if (use_hop_count and not (use_bisection_count or use_timeToSolution)):
      metric_new=float(sum(hop_count_distribution_new))/len(hop_count_distribution_new)
    elif (use_timeToSolution and not (use_hop_count or use_bisection_count)):
      metric_new=nopt.fitness_function_average_time_to_solution(connections)
    elif (use_bisection_count and not (use_hop_count or use_timeToSolution)):
      bisection_array=[]
      for bcount in range(number_of_picks):
	bisection_count=nopt.fitness_function_bisection_count_computers_and_routers(number_of_computers,number_of_routers,connections)
	bisection_array.append(bisection_count)
      metric_new=min(bisection_array)
    tracker_all.append(metric_new)
    
    if (use_simulated_annealing):
      # if metric_new<metric_best, then we have an improvement. Always accept that change.
      # if metric_new>metric_best, then we may accept that depending on random value between 0,1
      if (metric_new<metric_best):
	accept_change=True # this improvement was accepted without need to use exp()>random.random(). The close the temperature is to 0, the more likely this is the case
      else: # either the temperature is far from 0 and there is an improvement, or the change is a decrease in performance.
	try:
	  accept_change = math.exp((metric_best-metric_new)/temperature_value) > random.random()
	except OverflowError:    
	  print("metric_best-metric_new="+str(metric_best-metric_new))
	  print("temperature_value="+str(temperature_value))
	  print("ratio:"+str((metric_best-metric_new)/temperature_value))
	  exit()
      if ( accept_change ): # mathworld.wolfram.com/SimulatedAnnealing.html
	#print("improvement accepted at temperature index "+str(temperature_indx))
	tracker_mins.append(metric_new)
	tracker_mins_indx.append(temperature_indx)
	print("new best "+metric_name_label+" is "+str(metric_new)+" and old was "+str(metric_best))
	print("Total elapsed time: "+str(time.clock()-t_start)+" seconds")
	metric_best=metric_new
	connections_best=connections_new
	connections=connections_new
    else: # do not use simulated annealing
      if (metric_new<metric_best): # do not accept decrease in performance
	tracker_mins.append(metric_new)
	tracker_mins_indx.append(temperature_indx)
	print("new best "+metric_name_label+" is "+str(metric_new)+" and old was "+str(metric_best))
	print("Total elapsed time: "+str(time.clock()-t_start)+" seconds")
	metric_best=metric_new
	connections_best=connections_new
	connections=connections_new
	
    temperature_value=cooling_rate*temperature_value # geometric cooling schedule
    if (temperature_value<min_temp):
      print("temp="+str(temperature_value))
      temperature_indx=max_number_of_iterations+1
      break

    temperature_indx=temperature_indx+1
    t_metric_elapsed=time.clock()-t_metric_start
    #print("time to determine metric: "+str(t_metric_elapsed)+" seconds. Total elapsed time: "+str(time.clock()-t_start)+" seconds")
  nopt.done_searching(metric_initial,metric_best,connections_best,tracker_all,tracker_mins,tracker_mins_indx,metric_name_file,metric_name_label,t_start)
  nopt.draw_computer_and_router_graph_pictures(connections,"final")  

  all_search_results.append(metric_best)  
  if (metric_best<metric_best_of_all):
    metric_best_of_all=metric_best
    connections_best_of_all=connections_best
  
results_file=open("results_file",'w')
results_file.write(str(all_search_results))
results_file.close()
#os.system('sed -i 's/\]//g' results_file')
#os.system('sed -i 's/\[//g' results_file')
print min(all_search_results)
print metric_best_of_all
print connections_best_of_all