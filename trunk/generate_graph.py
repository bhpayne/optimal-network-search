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
import lib_network_optimization as nopt



#************ MAIN BODY *********************

# INPUT PARAMTERS
number_of_switches=10
number_of_computers=10
number_of_ports_per_computer=3
number_of_ports_per_switch=8

nopt.sanity_checks(number_of_switches,number_of_computers,number_of_ports_per_computer,number_of_ports_per_switch)

# create 1D array of computers given the ports\
const=-1
computers_arry=nopt.create_arrays_for_nodes(number_of_computers,number_of_ports_per_computer,const)
print("computers:")
#print(computers_arry)
#print("scrambled:")
random.shuffle(computers_arry) # decreases liklihood of putting computer into same switch redundantanly.
print(computers_arry)

const=1
switch_arry=nopt.create_arrays_for_nodes(number_of_switches,number_of_ports_per_switch,const)
print("switches:")
#print(switch_arry)
#random.shuffle(switch_arry)
print(switch_arry)

connections=[] # declare new list for the edge pairs

# plug computers into switches, avoiding redundancy
nopt.plug_computers_in_switches(computers_arry,switch_arry,connections)

# now we need to connect the remaining switches. Avoid redundancy while creating a fully-connected network
print("remaining switches:")
print(switch_arry)

nopt.plug_switches_into_remaining_switches(switch_arry,connections)

print("connections:")
print(connections)
if (len(switch_arry)==0):
  print("all switches are fully connected")
else:
  print("remaining empty switch ports:")
  print(switch_arry)

# at this point, if too many switches are given, there could exist switches which are connected to 0 or 1 computers. 
# to do: remove unused switches and switches connected to only one computer

nopt.writeGraphToFile(number_of_switches,number_of_computers,connections)

# EOF
