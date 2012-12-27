#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: make alterations to an existing graph

import lib_network_optimization as nopt # Ben's module 
#from random import sample  # for "choice" in determining connections
import random

# read existing graph
number_of_switches,number_of_computers,connections=nopt.readGraphFromFile()

# swap two port connections between computer-computer or computer-router or router-router
connections=nopt.make_alteration_swap_ports(number_of_switches,number_of_computers,connections)

# write updated graph
nopt.writeGraphToFile(number_of_switches,number_of_computers,connections)