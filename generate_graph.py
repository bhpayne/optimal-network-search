#!/usr/bin/python

import os

def create_graphviz_file():
  fil=open('network.gv', 'w')

  fil.write("##Command to produce the output: \"neato -Tpng thisfile.gv > thisfile.png\"\n")
  fil.write("graph G {\n")
  fil.write("node [shape=box,color=red,style=bold];  c1; c2; c3; c4; c5; c6; c7;\n")
  fil.write("node [shape=circle,fixedsize=true,width=0.9,color=blue,style=bold];  s1; s2; s3;\n")
  fil.write("     c1 -- s1;\n")
  fil.write("     c1 -- s2;\n")
  fil.write("     c1 -- s3;\n")
  fil.write("     c2 -- s1;\n")
  fil.write("     c2 -- s2;\n")
  fil.write("     c3 -- s1;\n")
  fil.write("     c3 -- s3;\n")
  fil.write("     c4 -- s3;\n")
  fil.write("     c5 -- s3;\n")
  fil.write("     c6 -- s1;\n")
  fil.write("     c6 -- s2;\n")
  fil.write("     c7 -- s2;\n")
  fil.write("     c7 -- s3;\n")
  fil.write("     overlap=false\n")
  fil.write("     label=\"optimized network test\\nlayed out by Graphviz\"\n")
  fil.write("     fontsize=12;\n")
  fil.write("}\n\n")
  fil.close()
  return

def generate_png_from_graphviz_file():
  os.system("neato -Tpng network.gv > network.png")
  return

switch_list =[
[1, 2, 3], # switch0 is connected to computers 1, 2, and 3
[0, 2, 4]]    # switch1 is connected to computers 0, 2 and 4

number_of_switches=2
number_of_computers=5
number_of_ports_per_computer=2

for switch_index,switch in enumerate(switch_list):
  this_switch_is_connected_to_computers=switch
  for computer in this_switch_is_connected_to_computers:
    print ("s"+str(switch_index)+"--c"+str(computer))

#create_graphviz_file

#generate_png_from_graphviz_file
