#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# the purpose of this script is to take a "connections" array and determine the number of hops between end points

import itertools          # for generating pairs of computers 

def find_distance(computerA,computerB,connections):
  print (str(computerA)+"--"+str(computerB)+": ")
  positions_for_computerA=find_positions_of_computer(connections,computerA)
  positions_for_computerB=find_positions_of_computer(connections,computerB)
  print ("locations of computer "+str(computerA)+": "+str(positions_for_computerA))
  print ("locations of computer "+str(computerB)+": "+str(positions_for_computerB))
  if ((len(positions_for_computerA)==1) and (len(positions_for_computerB)==1)): # both computers only have one connection
    #print ("locations of computer "+str(computerA)+": "+str(positions_for_computerA))
    #print ("locations of computer "+str(computerB)+": "+str(positions_for_computerB))
    if (positions_for_computerA[0][0]==positions_for_computerB[0][0]): # the computers are on the same switch
      print ("computer "+str(computerA)+" and "+str(computerB)+" are on the same switch")
      hop_distance=1
      return hop_distance
    #else: # computers each have one connection and they are on different switches
      ## is the switch computerA is connected to connected to the switch computerB is connected to?
      #for other_switch in 
      #if (positions_for_computerA[0][Y]==positions_for_computerB[0][X]):
  elif (len(positions_for_computerA)==1): # computer A has only one port
    for which_port_on_computerB in range(len(positions_for_computerB)):
      if (positions_for_computerA[0][0]==positions_for_computerB[which_port_on_computerB][0]): # the computers are on the same switch
	print ("computer "+str(computerA)+" and "+str(computerB)+" are on the same switch")
	hop_distance=1
	return hop_distance
      #else: # computerA has one port and the two computers are on different switches
  elif (len(positions_for_computerB)==1): # computer B has only one port
    for which_port_on_computerA in range(len(positions_for_computerA)):
      if (positions_for_computerB[0][0]==positions_for_computerA[which_port_on_computerA][0]): # the computers are on the same switch
	print ("computer "+str(computerA)+" and "+str(computerB)+" are on the same switch")
	hop_distance=1
	return hop_distance
      #else: # computerB has one port and the two computers are on different switches
  else: # both switches have more than one port
    for which_port_on_computerA in range(len(positions_for_computerA)):
      for which_port_on_computerB in range(len(positions_for_computerB)):
	if (positions_for_computerA[which_port_on_computerA][0]==positions_for_computerB[which_port_on_computerB][0]): # the computers are on the same switch
	  print ("computer "+str(computerA)+" and "+str(computerB)+" are on the same switch")
	  hop_distance=1
	  return hop_distance
        #else: # computers both have more than one port and the two computers are on different switches

  
def find_positions_of_computer(connections,computerA):
  all_positions_for_indx_A = list(get_positions(connections,computerA))
  # but we only care about computers with this index, not switches
  # ignore positions of the form (X,1,X)
  positions_for_computer=[]
  for position_indx in range(len(all_positions_for_indx_A)):
    if (all_positions_for_indx_A[position_indx][1]==0): # then this is a computer, not a switch
      positions_for_computer.append(all_positions_for_indx_A[position_indx])
  return positions_for_computer
  
# http://stackoverflow.com/questions/853023/how-can-i-find-the-locations-of-an-item-in-a-python-list-of-lists
def get_positions(xs, item): # "xs" is the list of lists, "item" is what you are looking for
    if isinstance(xs, list):
        for i, it in enumerate(xs):
            for pos in get_positions(it, item):
                yield (i,) + pos
    elif xs == item:
        yield ()
  
connections=[
[[0,1,2],[1]],
[[0,3,4],[0]]]


number_of_switches=len(connections)
number_of_computers=5

hop_array=[]
pair_array=list(itertools.combinations(range(number_of_computers), 2))
for pair_indx in range(len(pair_array)):
  hop_distance=find_distance(pair_array[pair_indx][0],pair_array[pair_indx][1],connections)
  hop_array.append(hop_distance)
print hop_array