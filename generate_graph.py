#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu
# see effbot.org/zone/python-list.htm

import os
from random import choice

def create_graphviz_file(computers,switches,connections):
  fil=open('network.gv', 'w')

  fil.write("##Command to produce the output: \"neato -Tpng thisfile.gv > thisfile.png\"\n")
  fil.write("graph G {\n")
  for computer in computers:
    fil.write("node [shape=box,color=red,style=bold];  c"+str(computer)+";\n")
  for switch in switches:  
    fil.write("node [shape=circle,fixedsize=true,width=0.9,color=blue,style=bold];  s"+str(switch)+";\n")

  for switch_index,switch in enumerate(connections):
    this_switch_is_connected_to_computers=switch
    for computer in this_switch_is_connected_to_computers:
      #print ("s"+str(switch_index)+"--c"+str(computer))
      fil.write("     s"+str(switch_index)+"--c"+str(computer)+";\n")
  fil.write("     overlap=false\n")
  fil.write("     label=\"optimized network test\\nlayed out by Graphviz\"\n")
  fil.write("     fontsize=12;\n")
  fil.write("}\n\n")
  fil.close()
  return


number_of_switches=100
number_of_computers=5
number_of_ports_per_computer=2
number_of_ports_per_switch=4

computers=range(number_of_computers)
switches=range(number_of_switches)

#connections =[
#[   1, 2, 3  ], # switch0 is connected to computers 1, 2, and 3
#[0,    2,   4]]    # switch1 is connected to computers 0, 2 and 4

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
  connections.append([]) # this creates a list of empty lists
for computer in computers:
  for port_indx in range(number_of_ports_per_computer):
    which_switch_this_computer_connects_to=choice(switches)
    if not computer in connections[which_switch_this_computer_connects_to]:     # if this computer is not already connected to this switch, then
      connections[which_switch_this_computer_connects_to].append(computer)      # connect it
#    else: # maybe a "while" would be better -- search for open switch

# if number of switches >> number of computers, then 
#   1) not all switches are used [and thus don't need to be drawn]
#   2) any given computer may not be able to connect to all other computers

print connections

create_graphviz_file(computers,switches,connections)

os.system("neato -Tpng network.gv > network.png")

# EOF