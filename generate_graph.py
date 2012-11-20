#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu
# the purpose of this script is to build a random but valid network of computers and switches
# --> avoid switch connecting to itself
# --> avoid computer connect to itself
# --> avoid redundant connections
# --> avoid switches with no computers connected to them
# --> avoid unconnected subset networks
# --> if (number of switches>1) then each switch must connect to at least one other switch

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

def hops_between_nodes(computer_pairs,connections):
  # option 1: exhaustive search
    #1a: start by filling out the known distance when computer A and B are plugged into the same switch
  #print connections
  #print computer_pairs
  for switch_index,switch_list in enumerate(connections):
    print switch_list
    pairs_on_this_switch=list(itertools.combinations(switch_list,2))
    print pairs_on_this_switch
  # option 2: take a random subset of computers and find the pair hopping distance

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

# the following fills all switch ports with connections to computers
# Problem: computer X can be connected to switch Y multiple times
# Problem: computer X may not be connected to any switch
###for switch_index in switches:
  ###print ("switch index="+str(switch_index))
  ###port_list=[]
  ###for port_index in range(number_of_ports_per_switch):
    ###port_list.append(choice(computers))
  ###connections.append(port_list)    

# use all the ports on each computer to connect to switches
# no computer should be connected to the same switch twice
# each computer should be connected to a switch
# --> the constraints center on the computer, not the switches. Thus we need to iterate through the list of computers
for indx in switches:
  connections.append([[],[]]) # this creates a list of empty lists [switch0, switch1,...] where switchX = [[computerK, computerB], [switchY]]
for computer in computers:
  for port_indx in range(number_of_ports_per_computer):
    find_port=True
    while find_port:
      which_switch_this_computer_connects_to=choice(switches)
      if (not computer in connections[which_switch_this_computer_connects_to][0]) and (len(connections[which_switch_this_computer_connects_to][0])+len(connections[which_switch_this_computer_connects_to][1])<number_of_ports_per_switch-1):     # if (this computer is not already connected to this switch) and (there are ), then
        connections[which_switch_this_computer_connects_to][0].append(computer)      # connect it
        find_port=False
for switch in switches:
  #for port_indx in range(number_of_ports_per_switch - len(connections[switch][0])): # fill in the remaining switch ports with connections to other switches
    find_port=True
    while find_port:
      which_switch_this_switch_connects_to=choice(switches)
      if (not switch in connections[which_switch_this_switch_connects_to][1]) and (not which_switch_this_switch_connects_to in connections[switch][1]): # and (which_switch_this_switch_connects_to != switch):     # if this switch is not already connected to this other switch), then
        if (which_switch_this_switch_connects_to==switch): 
          find_port=False
          break
        connections[which_switch_this_switch_connects_to][1].append(switch)      # connect it
        find_port=False
      if (len(connections[switch][0])+len(connections[switch][1]) == number_of_ports_per_switch): # this switch is full, no more connections should be made
        print switch
	find_port=False

# if number of switches >> number of computers, then 
#   1) not all switches are used [and thus don't need to be drawn]
#   2) any given computer may not be able to connect to all other computers
#   3? Having more than one path between two computers. Possible, but useful?

# solution to problem 1, not all switches are used [and thus don't need to be drawn]
newconnect=[]
#newconnect2=[]
newswitches=[]
#newswitches2=[]
for switch_indx in switches:
  if len(connections[switch_indx][0])>1: # remove switches with 0 or 1 computer connections
    newconnect.append(connections[switch_indx])
    newswitches.append(switch_indx)
    
for swi in range(len(newconnect)):
  print newconnect[swi]
    
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
