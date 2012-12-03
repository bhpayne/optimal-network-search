#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: measure the number of hops between two compute nodes

# output: 

import networkgraphio as ngio # Ben's module for graph input/output

number_of_switches,number_of_computers,connections=ngio.readGraphFromFile()

