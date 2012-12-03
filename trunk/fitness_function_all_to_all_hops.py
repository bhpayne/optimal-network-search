#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: measure the number of hops between all pairs of compute nodes

# output: 

import networkgraphio as ngio # Ben's module for graph input/output
import itertools           # for generating pairs of computers 

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

number_of_switches,number_of_computers,connections=ngio.readGraphFromFile()



