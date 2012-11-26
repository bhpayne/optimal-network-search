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
import random # for "random.shuffle"
from random import choice # for "choice" in determining connections
import itertools          # for generating pairs of computers 

def sanity_checks(number_of_switches,number_of_computers,number_of_ports_per_computer,number_of_ports_per_switch):
  # total number of ports on switches must be greater than number of compute nodes
  if ((number_of_switches*number_of_ports_per_switch)<number_of_computers):
    print ("total number of ports on switches must be greater than number of computers")
    print ("number of computers="+str(number_of_computers))
    print ("number of switches ="+str(number_of_switches))
    print ("number of ports on switch="+str(number_of_ports_per_switch))
    exit(1) # infinite loop would occur during search
  if ((number_of_switches*number_of_ports_per_switch)==number_of_computers) and (number_of_switches>1):
    print ("total number of ports on switches must be greater than number of computers")
    print ("number of computers="+str(number_of_computers))
    print ("number of switches ="+str(number_of_switches))
    print ("number of ports on switch="+str(number_of_ports_per_switch))
    exit(1) # infinite loop would occur during search
  if (number_of_switches==1) and (number_of_ports_per_switch==number_of_computers):
    print ("cross-bar network detected (number of ports per switch=number of computers, and number of switches=1")
    print ("no optimization to be performed")
  
def create_graphviz_file(number_of_switches,number_of_computers,connections):
  fil=open('network.gv', 'w')

  fil.write("##Command to produce the output: \"neato -Tpng thisfile.gv > thisfile.png\"\n")
  fil.write("graph G {\n")
  for computer in range(number_of_computers):
    fil.write("node [shape=box,color=red,style=bold];  c"+str(computer)+";\n")
  for switch in range(number_of_switches):  
    fil.write("node [shape=circle,fixedsize=true,width=0.9,color=blue,style=bold];  s"+str(switch)+";\n")

  for pair_index in range(len(connections)):
    if (connections[pair_index][0]<0): # negative value for computer
      nodeA="     c" 
    elif (connections[pair_index][0]>0): # positive value for switch
      nodeA="     s"
    else:
      print ("invalid value in connections array"+str(connections[pair_index][0]))
    if (connections[pair_index][0]<0): # negative value for computer
      nodeB="--c" 
    elif (connections[pair_index][0]>0): # positive value for switch
      nodeB="--s"
    else:
      print ("invalid value in connections array"+str(connections[pair_index][0]))
    #print ("s"+str(switch_index)+"--c"+str(computer))
    fil.write(nodeA+str(switch_index)+nodeB+str(computer)+";\n")
  fil.write("     overlap=false\n")
  fil.write("     label=\"optimized network test\\nlayed out by Graphviz\"\n")
  fil.write("     fontsize=12;\n")
  fil.write("}\n\n")
  fil.close()
  return

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

number_of_switches=10
number_of_computers=10
number_of_ports_per_computer=3
number_of_ports_per_switch=8

sanity_checks(number_of_switches,number_of_computers,number_of_ports_per_computer,number_of_ports_per_switch)

#switches=range(number_of_switches)


# create 1D array of computers given the ports\
const=-1
computers_arry=create_arrays_for_nodes(number_of_computers,number_of_ports_per_computer,const)
print("computers:")
#print(computers_arry)
#print("scrambled:")
random.shuffle(computers_arry)
print(computers_arry)

const=1
switch_arry=create_arrays_for_nodes(number_of_switches,number_of_ports_per_switch,const)
print("switches:")
#print(switch_arry)
random.shuffle(switch_arry)
print(switch_arry)

connections=[] # declare new list for the edge pairs
for computer_indx in range(len(computers_arry)):
  this_pair=[]
  this_pair.append(computers_arry[computer_indx])
  this_pair.append(switch_arry[computer_indx])
  connections.append(this_pair)

print("connections:")
print(connections)






#create_graphviz_file(computers,newconnect)

#hops_between_nodes(computer_pairs,newconnect)

#neato - filter for drawing undirected graphs
os.system("neato -Tpng network.gv > network_neato.png")
#twopi - filter for radial layouts of graphs
os.system("twopi -Tpng network.gv > network_twopi.png")
#circo - filter for circular layout of graphs
os.system("circo -Tpng network.gv > network_circo.png")
#fdp - filter for drawing undirected graphs
os.system("fdp -Tpng network.gv > network_fdp.png")
#sfdp - filter for drawing large undirected graphs
os.system("sfdp -Tpng network.gv > network_sfdp.png")


# EOF
