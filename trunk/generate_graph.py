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

  
def create_graphviz_file(computers,connections):
  fil=open('network.gv', 'w')

  fil.write("##Command to produce the output: \"neato -Tpng thisfile.gv > thisfile.png\"\n")
  fil.write("graph G {\n")
  for computer in computers:
    fil.write("node [shape=box,color=red,style=bold];  c"+str(computer)+";\n")
  for switch in range(len(connections)):  
    fil.write("node [shape=circle,fixedsize=true,width=0.9,color=blue,style=bold];  s"+str(switch)+";\n")

  for switch_index in range(len(connections)):
    this_switch_is_connected_to_computers=connections[switch_index][0]
    for computer in this_switch_is_connected_to_computers:
      #print ("s"+str(switch_index)+"--c"+str(computer))
      fil.write("     s"+str(switch_index)+"--c"+str(computer)+";\n")
    this_switch_is_connected_to_switches=connections[switch_index][1]
    for other_switch in this_switch_is_connected_to_switches:
      fil.write("     s"+str(switch_index)+"--s"+str(other_switch)+";\n")
  fil.write("     overlap=false\n")
  fil.write("     label=\"optimized network test\\nlayed out by Graphviz\"\n")
  fil.write("     fontsize=12;\n")
  fil.write("}\n\n")
  fil.close()
  return


number_of_switches=10
number_of_computers=10
number_of_ports_per_computer=3
number_of_ports_per_switch=8

sanity_checks(number_of_switches,number_of_computers,number_of_ports_per_computer,number_of_ports_per_switch)

computers=range(number_of_computers)
switches=range(number_of_switches)

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

connections=[] # declare new list











create_graphviz_file(computers,newconnect)

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
