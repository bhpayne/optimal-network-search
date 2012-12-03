#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# the purpose of this script is to build a random but valid network of computers and switches
# Constraints are
# --> avoid switch connecting to itself
# --> avoid computer connect to itself
# --> avoid redundant connections
# --> avoid switches with no computers connected to them
# --> avoid unconnected subset networks
# --> if (number of switches>1) then each switch must connect to at least one other switch

# method used: "connections" array is a set of sub-arrays, each representing an edge (computer-switch or switch-switch)
# number of computers, switches, and respective ports is static

# output: graphviz file to create picture of graph

# see effbot.org/zone/python-list.htm

import os
import random # "random.shuffle" for reordering computers and ports, switches and ports
from random import choice  # for "choice" in determining connections
import itertools           # for generating pairs of computers 
import networkgraphio as ngio # Ben's module for graph input/output

def sanity_checks(number_of_switches,number_of_computers,number_of_ports_per_computer,number_of_ports_per_switch):
  # total number of ports on switches must be greater than number of compute nodes
  if ((number_of_switches*number_of_ports_per_switch)<number_of_computers):
    print ("[FN] total number of ports on switches must be greater than number of computers")
    print ("number of computers="+str(number_of_computers))
    print ("number of switches ="+str(number_of_switches))
    print ("number of ports on switch="+str(number_of_ports_per_switch))
    exit(1) # infinite loop would occur during search
  if ((number_of_switches*number_of_ports_per_switch)==number_of_computers) and (number_of_switches>1):
    print ("[FN] total number of ports on switches must be greater than number of computers")
    print ("number of computers="+str(number_of_computers))
    print ("number of switches ="+str(number_of_switches))
    print ("number of ports on switch="+str(number_of_ports_per_switch))
    exit(1) # infinite loop would occur during search
  if (number_of_switches==1) and (number_of_ports_per_switch==number_of_computers):
    print ("[FN] cross-bar network detected (number of ports per switch=number of computers, and number of switches=1")
    print ("no optimization to be performed")
  
# the following is for the all-to-all network testing and currently isn't in use
def list_all_computer_pairs(number_of_computers):
  computers=range(number_of_computers)
  computer_pairs=[]
  pair_array=list(itertools.combinations(computers, 2))
  number_of_computer_pairs=len(pair_array)
# convert from list to array:
  for pair_indx in range(number_of_computer_pairs):
    pair_list=[]
    pair_list.append(pair_array[pair_indx][0])
    pair_list.append(pair_array[pair_indx][1])
    computer_pairs.append(pair_list)
# For n computers there are n*(n-1)/2 pairs
#>>> len(list(itertools.combinations(range(100), 2)))
#       4,950
#>>> len(list(itertools.combinations(range(1000), 2)))
#     499,500
#>>> len(list(itertools.combinations(range(1000000), 2))) # this fails, but the answer would be
# 499,999,500

def create_arrays_for_nodes(number_of_nodes,number_of_ports_per_node,const):
  node_arry=[]
  for node_indx in range(1,number_of_nodes+1): # the shift by +1 is to avoid use of "0" in numeric list
    for port_indx in range(number_of_ports_per_node):
      node_arry.append(node_indx*const)
  return node_arry

def plug_computers_in_switches(computers_arry,switch_arry,connections):
  for computer_indx in range(len(computers_arry)):
    found_valid_pair=0 # false
    while (not found_valid_pair):
      this_pair=[]
      this_pair.append(computers_arry[computer_indx])
      this_switch_port=choice(switch_arry)
      this_pair.append(this_switch_port)
      # if this pair already exists in connections (this computer is already plugged into the switch), try another switch
      keep_searching=1 # true
      for pair_indx in range(len(connections)):
	if ((connections[pair_indx][0]==this_pair[0]) and (connections[pair_indx][1]==this_pair[1])):
	  keep_searching=0 # false
	  break
      if (keep_searching==1): # for loop terminated without finding matching pair
	found_valid_pair=1 # computer-switch pair did not occur previously, so we found a valid pairing
	connections.append(this_pair)
	switch_arry.remove(this_switch_port) # remove switch port from pool of available ports

def plug_switches_into_remaining_switches(switch_arry,connections):
  loop_count=0
  while len(switch_arry)>1:
    if (loop_count>1000):
      print("[FN] probably redundant connections are all that is left")
      print("[FN] connections:")
      print(connections)
      print("[FN] remaining switches:")
      print(switch_arry)
      break
    loop_count=loop_count+1
    switchportA=choice(switch_arry)
    switchportB=choice(switch_arry)
    if (switchportA != switchportB):
      keep_searching=1 # true
      for pair_indx in range(number_of_computers*number_of_ports_per_computer,len(connections)): # skip the first set which is computer-switch pairs
	if (((connections[pair_indx][0]==switchportA) and (connections[pair_indx][1]==switchportB)) or ((connections[pair_indx][0]==switchportB) and (connections[pair_indx][1]==switchportA))):
	  keep_searching=0 # false
	  break
      if (keep_searching==1): # for loop terminated without finding matching pair
	this_pair=[]
	this_pair.append(switchportA)
	this_pair.append(switchportB)
	connections.append(this_pair)
	switch_arry.remove(switchportA) # remove switch port from pool of available ports
	switch_arry.remove(switchportB) # remove switch port from pool of available ports
	loop_count=0

#************ MAIN BODY *********************

# INPUT PARAMTERS
number_of_switches=10
number_of_computers=10
number_of_ports_per_computer=3
number_of_ports_per_switch=8

sanity_checks(number_of_switches,number_of_computers,number_of_ports_per_computer,number_of_ports_per_switch)

# create 1D array of computers given the ports\
const=-1
computers_arry=create_arrays_for_nodes(number_of_computers,number_of_ports_per_computer,const)
print("computers:")
#print(computers_arry)
#print("scrambled:")
random.shuffle(computers_arry) # decreases liklihood of putting computer into same switch redundantanly.
print(computers_arry)

const=1
switch_arry=create_arrays_for_nodes(number_of_switches,number_of_ports_per_switch,const)
print("switches:")
#print(switch_arry)
#random.shuffle(switch_arry)
print(switch_arry)

connections=[] # declare new list for the edge pairs

# plug computers into switches, avoiding redundancy
plug_computers_in_switches(computers_arry,switch_arry,connections)

# now we need to connect the remaining switches. Avoid redundancy while creating a fully-connected network
print("remaining switches:")
print(switch_arry)

plug_switches_into_remaining_switches(switch_arry,connections)

print("connections:")
print(connections)
if (len(switch_arry)==0):
  print("all switches are fully connected")
else:
  print("remaining empty switch ports:")
  print(switch_arry)

# at this point, if too many switches are given, there could exist switches which are connected to 0 or 1 computers. 
# to do: remove unused switches and switches connected to only one computer


#hops_between_nodes(computer_pairs,newconnect)

ngio.writeGraphToFile(number_of_switches,number_of_computers,connections)

# EOF
