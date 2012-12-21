import networkx as nx
import matplotlib.pyplot as plt
import random

number_of_routers=20
G=nx.cycle_graph(number_of_routers) # whatever graph you want to use here

all_routers=range(1,number_of_routers+1) 
print all_routers
random.shuffle(all_routers)
# now split this list into two parts of unequal size
random_number_of_routers= random.randint(0,number_of_routers)

print ("random number of routers="+str(random_number_of_routers))
left_partition=all_routers[0:random_number_of_routers]
right_partition=all_routers[random_number_of_routers:number_of_routers+1]

print left_partition
print right_partition

connections=G.edges()
bisection_count=0
print G.edges()
print "bisecting edges:"
for edge in connections:
  if (((edge[0]+1 in left_partition) and (edge[1]+1 in right_partition)) or ((edge[0]+1 in right_partition) and (edge[1]+1 in left_partition))):
    print edge
    bisection_count=bisection_count+1

print ("bisection count="+str(bisection_count))

node_color_list=[]
for router_indx in range(1,number_of_routers+1):
  if router_indx in left_partition:
    node_color_list.append('blue')
  else:
    node_color_list.append('red')
    
nx.draw(G,node_color=node_color_list)
plt.show()