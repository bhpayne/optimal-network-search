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
import pickle # serialize data output
# import cPickle as pickle # "upto 1000 times faster because it is in C"
import random # "random.shuffle" for reordering computers and ports, switches and ports
from random import choice  # for "choice" in determining connections
import itertools           # for generating pairs of computers 
  
def create_graphviz_file(number_of_switches,number_of_computers,connections):
  fil=open('network.gv', 'w')

  fil.write("##Command to produce the output: \"neato -Tpng thisfile.gv > thisfile.png\"\n")
  fil.write("graph G {\n")
  for computer in range(1,number_of_computers+1):
    fil.write("node [shape=box,color=red,style=bold];  c"+str(computer)+";\n")
  for switch in range(1,number_of_switches+1):  
    fil.write("node [shape=circle,fixedsize=true,width=0.9,color=blue,style=bold];  s"+str(switch)+";\n")

  for pair_index in range(len(connections)):
    if (connections[pair_index][0]<0): # negative value for computer
      nodeA="     c" 
    elif (connections[pair_index][0]>0): # positive value for switch
      nodeA="     s"
    else:
      print ("[FN] invalid value in connections array with nodeA"+str(connections[pair_index][0]))
    if (connections[pair_index][1]<0): # negative value for computer
      nodeB="--c" 
    elif (connections[pair_index][1]>0): # positive value for switch
      nodeB="--s"
    else:
      print ("[FN] invalid value in connections array with nodeB"+str(connections[pair_index][1]))
    #print ("s"+str(switch_index)+"--c"+str(computer))
    fil.write(nodeA+str(abs(connections[pair_index][0]))+nodeB+str(abs(connections[pair_index][1]))+";\n")
  fil.write("     overlap=false\n")
  fil.write("     label=\"optimized network test\\nlayed out by Graphviz\"\n")
  fil.write("     fontsize=12;\n")
  fil.write("}\n\n")
  fil.close()
  return

pkl_file=open('data.pkl','rb') # read
number_of_switches=pickle.load(pkl_file)
number_of_computers=pickle.load(pkl_file)
connections=pickle.load(pkl_file)
pkl_file.close()

create_graphviz_file(number_of_switches,number_of_computers,connections)

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
