#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: make alterations to an existing graph

import networkgraphio as ngio # Ben's module for graph input/output
#from random import sample  # for "choice" in determining connections
import random

# note: this can be replaced with
# http://networkx.lanl.gov/reference/generated/networkx.algorithms.swap.double_edge_swap.html#networkx.algorithms.swap.double_edge_swap
def swap_ports(number_of_switches,number_of_computers,connections):
  #edges_returned=sample(connections,2) # get two random edges from the connections array
  edgeA=connections.pop(random.randrange(len(connections))) # get a random edge from the connections array
  edgeB=connections.pop(random.randrange(len(connections)))
  edgeA_swapped=[]
  edgeB_swapped=[]
  edgeA_swapped.append(edgeA[0])  #   A =[X, Y] and B =[W, Z]
  edgeA_swapped.append(edgeB[1])  #   transform to
  edgeB_swapped.append(edgeB[0])  #   A'=[X, Z] and B'=[W, Y]
  edgeB_swapped.append(edgeA[1]) 
  connections.append(edgeA_swapped)
  connections.append(edgeB_swapped)
  return connections
  
def swap_multiple_switch_ports(number_of_switches,number_of_computers,connections):
  switches=range(1,number_of_switches+1)

# http://stackoverflow.com/questions/853023/how-can-i-find-the-locations-of-an-item-in-a-python-list-of-lists
def get_positions(xs, item): # "xs" is the list of lists, "item" is what you are looking for
    if isinstance(xs, list):
        for i, it in enumerate(xs):
            for pos in get_positions(it, item):
                yield (i,) + pos
    elif xs == item:
        yield ()

# read existing graph
number_of_switches,number_of_computers,connections=ngio.readGraphFromFile()

# swap two port connections between computer-computer or computer-router or router-router
connections=swap_ports(number_of_switches,number_of_computers,connections)

# write updated graph
ngio.writeGraphToFile(number_of_switches,number_of_computers,connections)