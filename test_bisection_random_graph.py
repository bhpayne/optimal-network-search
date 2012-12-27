import networkx as nx
import matplotlib.pyplot as plt
import random
import lib_network_optimization as nopt
import itertools

#************ MAIN BODY *********************

number_of_routers=3
number_of_ports_per_router=5
number_of_computers=10
number_of_ports_per_computer=1
number_of_iterations=1000 # how many evolutions to make
random_network_search_limit=1000 # used for random graph generation
valid_path_search_limit=100 
search_mod_alert=20 # how often to display that no path modification has been found
nopt.sanity_checks(number_of_routers,number_of_computers,number_of_ports_per_computer,number_of_ports_per_router)
connections = nopt.generate_random_network(number_of_computers,number_of_ports_per_computer,number_of_routers,number_of_ports_per_router,random_network_search_limit)

nopt.draw_graph_pictures(connections,"initial")

all_computers=range(1,number_of_computers+1)
all_computers=[comp*-1 for comp in all_computers]
all_routers=range(1,number_of_routers+1)
random.shuffle(all_computers) # for the purpose of selecting a random set of half the computers
if ((number_of_computers%2)==0):
  left_partition_computers = all_computers[0:number_of_computers/2]
  right_partition_computers = all_computers[number_of_computers/2:number_of_computers]
else:
  left_partition_computers = all_computers[0:(number_of_computers+1)/2]
  right_partition_computers = all_computers[(number_of_computers+1)/2:number_of_computers]
print ("computer partitions:")
print left_partition_computers
print right_partition_computers
# 1) grab a random number of switches
random.shuffle(all_routers)
# now split this list into two parts
random_number_of_routers=random.randint(0,number_of_routers)
left_partition_routers=all_routers[0:random_number_of_routers]
right_partition_routers=all_routers[random_number_of_routers:number_of_routers]
print ("router partitions:")
print left_partition_routers
print right_partition_routers
# 2) for each edge in connections, are the two values in two partitions?
left_partition=[]
left_partition.append(left_partition_routers)
left_partition.append(left_partition_computers)
right_partition=[]
right_partition.append(right_partition_routers)
right_partition.append(right_partition_computers)
left_partition = list(itertools.chain(*left_partition))
right_partition= list(itertools.chain(*right_partition))
print ("left partition:")
print left_partition
#print new_left
print ("right partition:")
print right_partition
#print new_right
bisection_count=0
print "bisecting edges:"
for edge in connections:
  #print ("first element of edge:"+str(edge[0])+" and second:"+str(edge[1]))
  if (((edge[0] in left_partition) and (edge[1] in right_partition)) or ((edge[0] in right_partition) and (edge[1] in left_partition))):
    print edge
    bisection_count=bisection_count+1

print ("bisection count="+str(bisection_count))

#node_color_list=[]
#for router_indx in range(1,number_of_routers+1):
  #if router_indx in left_partition:
    #node_color_list.append('blue')
  #else:
    #node_color_list.append('red')
    
#nx.draw(G,node_color=node_color_list)
#plt.show()

nopt.draw_graph_pictures(connections,"final")  



