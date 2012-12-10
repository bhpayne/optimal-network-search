import networkx as nx
import matplotlib.pyplot as plt
import os
import random # "random.shuffle" for reordering computers and ports, routers and ports
from random import choice  # for "choice" in determining connections
import pickle # serialize data output
# import cPickle as pickle # "upto 1000 times faster because it is in C"
import itertools           # for generating pairs of computers 

def fitness_function_find_all_compute_hop_lengths(number_of_computers,connections):
  all_pairs=list(itertools.combinations(range(1,number_of_computers+1), 2))

  all_lengths=[]
  for pair_indx in range(len(all_pairs)):
    computerA=all_pairs[pair_indx][0]*-1
    computerB=all_pairs[pair_indx][1]*-1
    # create a new graph with only compute nodes A, B, and routers.
    connections_only_AB=[]
    for edgeindx in range(len(connections)):
      if (connections[edgeindx][0]==computerA or connections[edgeindx][1]==computerA or connections[edgeindx][0]==computerB or connections[edgeindx][1]==computerB or (connections[edgeindx][0]>0 and connections[edgeindx][1]>0 )):
	add_this_pair=[]
	add_this_pair.append(connections[edgeindx][0])
	add_this_pair.append(connections[edgeindx][1])
	connections_only_AB.append(add_this_pair)
    G=convert_connections_to_G(connections_only_AB)  
    # http://networkx.lanl.gov/reference/generated/networkx.algorithms.shortest_paths.generic.shortest_path_length.html#networkx.algorithms.shortest_paths.generic.shortest_path_length
    length_between_compute_nodes=nx.shortest_path_length(G,source=computerA,target=computerB)
    #print length_compute_nodes
    all_lengths.append(length_between_compute_nodes)
  return all_lengths

def convert_connections_to_G(connections):
  G=nx.Graph()
  G.clear()
  G=nx.Graph()
  G.add_edges_from(connections)
  return G

# output: connections
# note: this can be replaced with
# http://networkx.lanl.gov/reference/generated/networkx.algorithms.swap.double_edge_swap.html#networkx.algorithms.swap.double_edge_swap
def make_alteration_swap_ports(number_of_routers,number_of_computers,connections):
  edgeA=connections.pop(random.randrange(len(connections))) # get a random edge from the connections array
  edgeB=connections.pop(random.randrange(len(connections)))
  edgeA_swapped=[]
  edgeB_swapped=[]
  edgeA_swapped.append(edgeA[0])  #   A =[X, Y] and B =[W, Z]
  edgeA_swapped.append(edgeB[1])  #   transform to
  edgeB_swapped.append(edgeB[0])  #   A'=[X, Z] and B'=[W, Y]
  edgeB_swapped.append(edgeA[1]) 
  connections.append(edgeA_swapped)
  connections.append(edgeB_swapped)
  return connections

  
#def swap_multiple_router_ports(number_of_routers,number_of_computers,connections):
  #routers=range(1,number_of_routers+1)

## http://stackoverflow.com/questions/853023/how-can-i-find-the-locations-of-an-item-in-a-python-list-of-lists
#def get_positions(xs, item): # "xs" is the list of lists, "item" is what you are looking for
    #if isinstance(xs, list):
        #for i, it in enumerate(xs):
            #for pos in get_positions(it, item):
                #yield (i,) + pos
    #elif xs == item:
        #yield ()
  
def sanity_checks(number_of_routers,number_of_computers,number_of_ports_per_computer,number_of_ports_per_router):
  # total number of ports on routers must be greater than number of compute nodes
  if ((number_of_routers*number_of_ports_per_router)<number_of_computers):
    print ("[Sanity Error] total number of ports on routers must be greater than number of computers")
    print ("number of computers="+str(number_of_computers))
    print ("number of routers ="+str(number_of_routers))
    print ("number of ports on router="+str(number_of_ports_per_router))
    exit(1) # infinite loop would occur during search due to insufficient connections
  if ((number_of_routers*number_of_ports_per_router)==number_of_computers) and (number_of_routers>1):
    print ("[Sanity Error] total number of ports on routers must be greater than number of computers")
    print ("number of computers="+str(number_of_computers))
    print ("number of routers ="+str(number_of_routers))
    print ("number of ports on router="+str(number_of_ports_per_router))
    exit(1) # infinite loop would occur during search due to disconnected routers
  if (number_of_routers==1) and (number_of_ports_per_router==number_of_computers):
    print ("[Sanity Error] cross-bar network detected")
    print ("(number of ports per router)==(number of computers) and (number of routers==1)")
    print ("no optimization to be performed")
    exit(1)
  if ((number_of_routers*number_of_ports_per_router)!=(number_of_computers*number_of_ports_per_computer)):
    print ("[Sanity Warning] (number of routers)*(number of ports per router) does not equal (number of computers)*(number of ports per computer)")
    print ("Therefore, you aren't using all available connections")

def create_graphviz_file(number_of_routers,number_of_computers,connections):
  fil=open('network.gv', 'w')

  fil.write("##Command to produce the output: \"neato -Tpng thisfile.gv > thisfile.png\"\n")
  fil.write("graph G {\n")
  for computer in range(1,number_of_computers+1):
    fil.write("node [shape=box,color=red,style=bold];  c"+str(computer)+";\n")
  for router in range(1,number_of_routers+1):  
    fil.write("node [shape=circle,fixedsize=true,width=0.9,color=blue,style=bold];  r"+str(router)+";\n")

  for pair_index in range(len(connections)):
    if (connections[pair_index][0]<0): # negative value for computer
      nodeA="     c" 
    elif (connections[pair_index][0]>0): # positive value for router
      nodeA="     r"
    else:
      print ("[Sanity] invalid value in connections array with nodeA"+str(connections[pair_index][0]))
    if (connections[pair_index][1]<0): # negative value for computer
      nodeB="--c" 
    elif (connections[pair_index][1]>0): # positive value for router
      nodeB="--r"
    else:
      print ("[Sanity] invalid value in connections array with nodeB"+str(connections[pair_index][1]))
    #print ("s"+str(router_index)+"--c"+str(computer))
    fil.write(nodeA+str(abs(connections[pair_index][0]))+nodeB+str(abs(connections[pair_index][1]))+";\n")
  fil.write("     overlap=false\n")
  fil.write("     label=\"optimized network test\\nlayed out by Graphviz\"\n")
  fil.write("     fontsize=12;\n")
  fil.write("}\n\n")
  fil.close()
  return
  
  

def writeGraphToFile(number_of_routers,number_of_computers,connections):
  output=open('graph.pkl','wb')
  pickle.dump(number_of_routers,output)
  pickle.dump(number_of_computers,output)
  pickle.dump(connections,output)
  output.close()

def readGraphFromFile():
  pkl_file=open('graph.pkl','rb') # read
  number_of_routers=pickle.load(pkl_file)
  number_of_computers=pickle.load(pkl_file)
  connections=pickle.load(pkl_file)
  pkl_file.close()
  return number_of_routers,number_of_computers,connections

  
  
  
  
def draw_graph_pictures(connections,name):
  G=convert_connections_to_G(connections)
  nx.draw(G)
  #plt.show()
  plt.savefig("networkx_draw_"+name+".png")
  #nx.draw_random(G)
  ##plt.show()
  #plt.savefig("networkx_random_"+name+".png")
  #nx.draw_circular(G)
  ##plt.show()
  #plt.savefig("networkx_circular_"+name+".png")
  #nx.draw_spectral(G)
  ##plt.show()
  #plt.savefig("networkx_spectral_"+name+".png")
  plt.close()
  
  
  
def create_arrays_for_nodes(number_of_nodes,number_of_ports_per_node,const):
  node_arry=[]
  for node_indx in range(1,number_of_nodes+1): # the shift by +1 is to avoid use of "0" in numeric list
    for port_indx in range(number_of_ports_per_node):
      node_arry.append(node_indx*const)
  return node_arry

def plug_computers_in_routers(computers_arry,router_arry,connections):
  for computer_indx in range(len(computers_arry)):
    found_valid_pair=0 # false
    while (not found_valid_pair):
      this_pair=[]
      this_pair.append(computers_arry[computer_indx])
      this_router_port=choice(router_arry)
      this_pair.append(this_router_port)
      # if this pair already exists in connections (this computer is already plugged into the router), try another router
      keep_searching=1 # true
      for pair_indx in range(len(connections)):
	if ((connections[pair_indx][0]==this_pair[0]) and (connections[pair_indx][1]==this_pair[1])):
	  keep_searching=0 # false
	  break
      if (keep_searching==1): # for loop terminated without finding matching pair
	found_valid_pair=1 # computer-router pair did not occur previously, so we found a valid pairing
	connections.append(this_pair)
	router_arry.remove(this_router_port) # remove router port from pool of available ports

# depends on: no other functions
# returns: connections
def plug_routers_into_remaining_routers(number_of_computers,number_of_ports_per_computer,router_arry,connections,search_loop_limit):
  loop_count=0
  while len(router_arry)>1:
    if (loop_count>search_loop_limit):
      print("[PRIRR] probably redundant connections are all that is left")
      print("[PRIRR] connections:")
      print(connections)
      print("[PRIRR] remaining routers:")
      print(router_arry)
      break
    loop_count=loop_count+1
    routerportA=choice(router_arry)
    routerportB=choice(router_arry)
    if (routerportA != routerportB):
      keep_searching=1 # true
      for pair_indx in range(number_of_computers*number_of_ports_per_computer,len(connections)): # skip the first set which is computer-router pairs
	if (((connections[pair_indx][0]==routerportA) and (connections[pair_indx][1]==routerportB)) or ((connections[pair_indx][0]==routerportB) and (connections[pair_indx][1]==routerportA))):
	  keep_searching=0 # false
	  break
      if (keep_searching==1): # for loop terminated without finding matching pair
	this_pair=[]
	this_pair.append(routerportA)
	this_pair.append(routerportB)
	connections.append(this_pair)
	router_arry.remove(routerportA) # remove router port from pool of available ports
	router_arry.remove(routerportB) # remove router port from pool of available ports
	loop_count=0

# depends on "sanity_checks" "create_arrays_for_nodes" "plug_computers_in_routers" "plug_routers_into_remaining_routers"
# output: "connections"
def generate_random_network(number_of_computers,number_of_ports_per_computer,number_of_routers,number_of_ports_per_router,search_loop_limit):
  sanity_checks(number_of_routers,number_of_computers,number_of_ports_per_computer,number_of_ports_per_router)

  print_random_network=0 # false
  
  # create 1D array of computers given the ports\
  const=-1
  computers_arry=create_arrays_for_nodes(number_of_computers,number_of_ports_per_computer,const)
  if print_random_network:
    print("[GRN] computers:")
  #print(computers_arry)
  #print("scrambled:")
  random.shuffle(computers_arry) # decreases liklihood of putting computer into same router redundantanly.
  if print_random_network:
    print(computers_arry)

  const=1
  router_arry=create_arrays_for_nodes(number_of_routers,number_of_ports_per_router,const)
  if print_random_network:
    print("[GRN] routers:")
  #print(router_arry)
  #random.shuffle(router_arry)
  if print_random_network:
    print(router_arry)

  connections=[] # declare new list for the edge pairs

  # plug computers into routers, avoiding redundancy
  plug_computers_in_routers(computers_arry,router_arry,connections)

  # now we need to connect the remaining routers. Avoid redundancy while creating a fully-connected network
  if print_random_network:
    print("[GRN] remaining routers:")
    print(router_arry)

  plug_routers_into_remaining_routers(number_of_computers,number_of_ports_per_computer,router_arry,connections,search_loop_limit)

  if print_random_network:
    print("[GRN] connections:")
    print(connections)
  if (len(router_arry)==0):
    print("[GRN] all routers are fully connected")
  else:
    print("[GRN] remaining empty router ports:")
    print(router_arry)

  # at this point, if too many routers are given, there could exist routers which are connected to 0 or 1 computers. 
  # to do: remove unused routers and routers connected to only one computer
  return connections