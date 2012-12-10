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
import lib_network_optimization as nopt


number_of_switches,number_of_computers,connections=nopt.readGraphFromFile()
  
nopt.create_graphviz_file(number_of_switches,number_of_computers,connections)

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
