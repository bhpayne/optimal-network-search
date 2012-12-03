#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: make alterations to an existing graph

import networkgraphio as ngio # Ben's module for graph input/output
from random import choice  # for "choice" in determining connections

def swap_computer_ports(number_of_switches,number_of_computers,connections):
  computers=range(1,number_of_computers+1)
  all_connect_data_flattened=sum(connections,[]) # only flattens list of lists
  found_valid_pair_to_switch=0 # false
  while (not found_valid_pair_to_switch):
    found_multiport_computer=0 # false
    while (not found_multiport_computer):
      computerA=choice(computers)*-1
      # this computer must have more than one port
      if (all_connect_data_flattened.count(computerA)>1): # computerA has more than one port
	found_multiport_computer=1 # true
	break
    # choose a random port for computerA to work with
    all_positions_for_computerA = list(get_positions(connections,computerA))
    which_A_to_switch=choice(all_positions_for_computerA)
    
    found_valid_second_computer=0 # false
    while (not found_valid_second_computer):
      computerB=choice(computers)*-1
      # this computer cannot be the same as computerA
      if (computerB != computerA):
	found_valid_second_computer=1 # true
	break
    # computerA and computerB cannot already be connected to the same switch
    found_port_on_second_computer=0 # false
    while (not found_port_on_second_computer):
      #if (computerB is not on same switch as computerA)
      break  
    break
  
  # now we know computerA and computerB.
  # choose which of the instances of each to switch
  all_positions_for_computerB = list(get_positions(connections,computerA))
  #print computerA
  #print computerB
  #print connections
  #print all_positions_for_computerA
  which_B_to_switch=choice(all_positions_for_computerB)
  #print which_A_to_switch[0]
  
  # swap the connections
  
  
  return connections
  
def swap_one_switch_port(number_of_switches,number_of_computers,connections):
  switches=range(1,number_of_switches+1)
  
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

# swap two port connections between computers
connections=swap_computer_ports(number_of_switches,number_of_computers,connections)

# write updated graph
ngio.writeGraphToFile(number_of_switches,number_of_computers,connections)