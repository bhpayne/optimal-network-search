import networkx as nx
import matplotlib.pyplot as plt
import random

number_of_routers=20
G=nx.cycle_graph(number_of_routers) # whatever graph you want to use here

all_routers=range(1,number_of_routers+1) 
random.shuffle(all_routers)
# now split this list into two parts of unequal size
random_number_of_routers=random.randint(0,number_of_routers)

left_partition_routers=all_routers[0:random_number_of_routers]
right_partition_routers=all_routers[random_number_of_routers+1:number_of_routers]

node_color_list=[]
for router_indx in range(1,number_of_routers+1):
  if router_indx in left_partition_routers:
    node_color_list.append('blue')
  else:
    node_color_list.append('red')
    
nx.draw(G,node_color=node_color_list)
plt.show()
