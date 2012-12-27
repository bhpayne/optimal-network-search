import networkx as nx
import matplotlib.pyplot as plt
import os
import random # "random.shuffle" for reordering computers and ports, routers and ports
from random import choice  # for "choice" in determining connections
import pickle # serialize data output
# import cPickle as pickle # "upto 1000 times faster because it is in C"
import itertools           # for generating pairs of computers 


#import networkx as nx
#G=nx.Graph()
#G.add_edges_from([(1,2),(2,3),(1,3)])


# https://en.wikipedia.org/wiki/Cut_(graph_theory)
# https://en.wikipedia.org/wiki/Connectivity_(graph_theory)
# https://en.wikipedia.org/wiki/Minimum_cut
# https://en.wikipedia.org/wiki/Graph_partitioning_problem
def fitness_function_bisection_count(number_of_computers,number_of_routers,connections):
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
  #print ("computer partitions:")
  #print left_partition_computers
  #print right_partition_computers

  # 20121220: I don't think the algorithm below has any strong advantages yet, so I'm going to due a brute-force search
  #**********************************
  ## now that we know which computers we care about, grab the routers pluged into those computers
  ## routers with computers only in the "left" set are assigned to the new "left (routers-only)" set; similarly routers with computers only in the "right" set are assigned to "right (routers-only)"
  ## some routers will have computers plugged into both "left" and "right" sets. Assign these routers to "left" and "right" randomly (via a coin flip biased on number of left and right computers)
  ## does a given router belong in "left" or "right" set?
  ## pseudo-code for algorithm:
  #for this_router in all_routers:
    #if (this_router connects only with other routers):
      #place this_router in random.choice(left_side or right_side)
    #elif (this_router connects to computers only on left_side):
      #place this_router in left_side
    #elif (this_router connects to computers only on right_side):
      #place this_router in right_side
    #else: # this_router connects with computers on both left and right sides
      #place this_router in (left_side or right_side, bias based on number of computers on left_side versus right_side)
  #count number of connections between left_side and right_side
  #**********************************
  # Brute-force bisection search
  #OLD: left_partition_routers=random.sample(all_routers,random.randint(0,number_of_routers) # this works, but I'm not sure how to get the right half elegantly.
  # 1) grab a random number of switches

  random.shuffle(all_routers)
  # now split this list into two parts
  random_number_of_routers=random.randint(0,number_of_routers)
  left_partition_routers=all_routers[0:random_number_of_routers]
  right_partition_routers=all_routers[random_number_of_routers:number_of_routers]
  #print ("router partitions:")
  #print left_partition_routers
  #print right_partition_routers
  # 2) for each edge in connections, are the two values in two partitions?
  left_partition=[]
  left_partition.append(left_partition_routers)
  left_partition.append(left_partition_computers)
  right_partition=[]
  right_partition.append(right_partition_routers)
  right_partition.append(right_partition_computers)
  left_partition = list(itertools.chain(*left_partition)) # flattens list of lists into a list
  right_partition= list(itertools.chain(*right_partition))
  #print ("left partition:")
  #print left_partition
  #print ("right partition:")
  #print right_partition
  bisection_count=0
  #print "bisecting edges:"
  for edge in connections:
    #print ("first element of edge:"+str(edge[0])+" and second:"+str(edge[1]))
    if (((edge[0] in left_partition) and (edge[1] in right_partition)) or ((edge[0] in right_partition) and (edge[1] in left_partition))):
      #print edge
      bisection_count=bisection_count+1
  return bisection_count
  #print ("bisection count="+str(bisection_count))
  

  
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

def make_alteration_remove_router_router_edge(number_of_routers,number_of_computers,connections,number_of_ports_per_router,random_network_search_limit):
  flattened_connections = list(itertools.chain(connections))

  valid_removal=False
  slimit=0
  while ((not valid_removal) and (slimit<random_network_search_limit)):
    found_router_with_enough_ports_used=False
    search_indx=0
    while ((not found_router_with_enough_ports_used) and (search_indx<number_of_routers)):
      routerA=random.randint(1,number_of_routers) # pick a random router A
      if (flattened_connections.count(routerA)>2):    # does router A have more than 2 connections?
	found_router_with_enough_ports_used=True
	break
      else:
	search_indx=search_indx+1
    if (search_indx==number_of_routers):
      print('didn\'t find a router to disconnect after '+str(number_of_routers)+' tries')
      return connections

    # at this point we have found routerA and it has more than 2 connections
    found_router_connected_to_A=False
    search_indx=0
    # MORE WORK TO BE DONE HERE, BUT I'M TIRED
    #while (not found_router_connected_to_A) and (search_indx<number_of_routers)
      # pick a random router B connected to A
      # does router B have more than 2 connections?

    # remove [A,B] from connections
    # check that this doesn't break the network: test paths between all computers
    try:
      hop_count_distribution=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections)
      valid_removal=True
      break
    except nx.NetworkXNoPath:
      print("this removal segments the network")
      valid_removal=False
      slimit=slimit+1
  return connections
  
def make_alteration_add_router_router_edge(number_of_routers,connections,number_of_ports_per_router,random_network_search_limit):
  flattened_connections = list(itertools.chain(connections))
  found_router_with_empty_ports=False
  search_indx=0
  while ((not found_router_with_empty_ports) and (search_indx<number_of_routers)):
    routerA=random.randint(1,number_of_routers) # pick a random router A
    if (flattened_connections.count(routerA)<number_of_ports_per_router):    # does router A have open ports?
      found_router_with_empty_ports=True
      break
    else:
      search_indx=search_indx+1
  if (search_indx==number_of_routers):
    print('didn\'t find a router to connect after '+str(number_of_routers)+' tries')
    return connections

  # at this point we have found routerA and it has open ports
  found_second_router_with_empty_ports=False
  search_indx=0
  while ((not found_second_router_with_empty_ports) and (search_indx<number_of_routers)):
    routerB=random.randint(1,number_of_routers) # pick a random router B
    if ((flattened_connections.count(routerB)<number_of_ports_per_router) and (routerA != routerB)):    # does router B have open ports and is distinct from A?
      found_second_router_with_empty_ports=True
      break
    else:
      search_indx=search_indx+1
  if (search_indx==number_of_routers):
    print('didn\'t find a second router to connect after '+str(number_of_routers)+' tries')
    return connections
  #print('routerA: '+str(routerA)+' and routerB: '+str(routerB))
  connections.append([routerA,routerB])    # add connection between A,B
  return connections
  
# output: connections
# note: this cannot be replaced with
# http://networkx.lanl.gov/reference/generated/networkx.algorithms.swap.double_edge_swap.html#networkx.algorithms.swap.double_edge_swap
# since ((router-computer) and (router-computer)) would swap to ((router-router) and (computer-computer)
def make_alteration_swap_ports(number_of_routers,number_of_computers,connections,random_network_search_limit):
  # we assume no connection exist of the form computer-computer
  # we need to make alterations which do not introduce computer-computer edges.
  edgeA=connections.pop(random.randrange(len(connections))) # get a random edge from the connections array
  search_indx=0
  if ((edgeA[0]<0) and (edgeA[1]<0)):
    print("ERROR: computer-computer connection found!")
    print edgeA
    #exit()
  elif ((edgeA[0]>0) and (edgeA[1]>0)): # if edgeA is router-router, then it doesn't matter whether edgeB is r-r, c-r, or r-c
    edgeB=connections.pop(random.randrange(len(connections)))
  else: 
    if ((edgeA[0]>0) and (edgeA[1]<0)):  # if edgeA is r-c, then edgeB can be either r-r or c-r. edgeB cannot be r-c
      found_valid_edge_pair=False
      while ((not found_valid_edge_pair) and (search_indx<random_network_search_limit)):
	edgeB=connections.pop(random.randrange(len(connections)))
	if ((edgeB[0]>0) and (edgeB[1]>0)) or ((edgeB[0]<0) and (edgeB[1]>0)):
	  found_valid_edge_pair=True
	  search_indx=0
	  break
	else:
	  connections.append(edgeB)
	  search_indx=search_indx+1
    if ((edgeA[0]<0) and (edgeA[1]>0)):  # if edgeA is c-r, then edgeB can be either r-r or r-c. edgeB cannot be c-r
      found_valid_edge_pair=False
      while ((not found_valid_edge_pair) and (search_indx<random_network_search_limit)):
	edgeB=connections.pop(random.randrange(len(connections)))
	if ((edgeB[0]>0) and (edgeB[1]>0)) or ((edgeB[0]>0) and (edgeB[1]<0)):
	  found_valid_edge_pair=True
	  search_indx=0
	  break
	else:
	  connections.append(edgeB)
	  search_indx=search_indx+1
  if (search_indx==random_network_search_limit):
    print("ERROR: valid edge pair not found during swap search")
    return connections    
  #print("edgeA before:")
  #print edgeA
  #print("edgeB before:")
  #print edgeB
  
  edgeA_swapped=[]
  edgeB_swapped=[]
  edgeA_swapped.append(edgeA[0])  #   A =[X, Y] and B =[W, Z]            X--Y     X  Y
  edgeA_swapped.append(edgeB[0])  #   transform to                            ==> |  |
  edgeB_swapped.append(edgeA[1])  #   A'=[X, W] and B'=[Y, Z]            W--Z     W  Z
  edgeB_swapped.append(edgeB[1]) 
  #print("edgeA after:")
  #print edgeA_swapped
  #print("edgeB after:")
  #print edgeB_swapped
  
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
  if ((number_of_computers%1)!=0):
    print ("[Sanity Error] number of computers must be an integer")
    exit(1)
  if ((number_of_ports_per_computer%1)!=0):
    print ("[Sanity Error] number of ports per computer must be an integer")
    exit(1)
  if ((number_of_routers%1)!=0):
    print ("[Sanity Error] number of routers must be an integer")
    exit(1)
  if ((number_of_ports_per_router%1)!=0):
    print ("[Sanity Error] number of ports per router must be an integer")
    exit(1)
  if (number_of_computers<=2):
    print ("[Sanity Error] number of computers must greater than 2")
    exit(1)
  if (number_of_ports_per_computer<=0):
    print ("[Sanity Error] number of ports per computer must be greater than 0")
    exit(1)
  if (number_of_routers<=1):
    print ("[Sanity Error] number of routers must be greater than 1")
    exit(1)
  if (number_of_ports_per_router<=2):
    print ("[Sanity Error] number of ports per router must be greater than 2")
    exit(1)
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
  compute_color='red'
  router_color='blue'
  node_color_list=color_graph_nodes(G,compute_color,router_color)
  nx.draw(G,node_color=node_color_list)
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
  Gviz=G
  nx.draw_graphviz(Gviz,prog='neato')
  # the following doesn't work because it gets over-written by write_dot()
  #stream=file('networkx_graphviz_'+name+'.dot','w')
  #stream.write('# neato -Tpng networkx_graphviz_'+name+'.dot > networkx_graphviz_'+name+'.png')
  #stream.close()
  nx.write_dot(Gviz,'networkx_graphviz_'+name+'.dot')
  os.system('neato -Tpng networkx_graphviz_'+name+'.dot > networkx_graphviz_'+name+'.png')
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

# as an example,
# compute_color='red'
# router_color='blue'
def color_graph_nodes(G,compute_color,router_color):
  all_nodes=G.nodes()
  node_color_list=[]
  for indx in range(len(all_nodes)):
    if (all_nodes[indx]<0):
      node_color_list.append(compute_color)
    elif (all_nodes[indx]>0):
      node_color_list.append(router_color)
    else:
      print("invalid node value")
      exit(1)
  return node_color_list
	
# http://networkx.lanl.gov/reference/generators.html
def generate_2D_mesh_network(number_of_rows,number_of_columns):
  if ((number_of_rows<2) or (number_of_columns<2)):
    print("[G2DMN] insufficient number of rows or columns. Minimum size is 2x2")
  # http://networkx.lanl.gov/reference/generated/networkx.generators.classic.grid_2d_graph.html
  Gcoordinates=nx.grid_2d_graph(number_of_rows,number_of_columns, periodic=False)
  # http://networkx.lanl.gov/reference/generated/networkx.relabel.convert_node_labels_to_integers.html#networkx.relabel.convert_node_labels_to_integers
  G=nx.convert_node_labels_to_integers(Gcoordinates,first_label=1)
  # Add compute nodes to each router
  # G.number_of_nodes()==number_of_rows*number_of_columns
  for indx in range(1,G.number_of_nodes()+1):
    G.add_edge(indx,indx*-1)
  #return G
  connections=G.edges()
  return connections
  
# as an example,
# dimensions=[2,3,5]
# toroidal_true_mesh_false=True
def generate_ND_toroidal_or_mesh_network(dimensions,toroidal_true_mesh_false):
  # http://networkx.lanl.gov/reference/generated/networkx.generators.classic.grid_graph.html
  Gcoordinates=nx.grid_graph(dim=dimensions, periodic=toroidal_true_mesh_false)
  G=nx.convert_node_labels_to_integers(Gcoordinates,first_label=1)
  # Add compute nodes to each router
  for indx in range(1,G.number_of_nodes()+1):
    G.add_edge(indx,indx*-1)
  #return G
  connections=G.edges()
  return connections

	
# depends on "sanity_checks" "create_arrays_for_nodes" "plug_computers_in_routers" "plug_routers_into_remaining_routers"
# output: "connections"
def generate_random_network(number_of_computers,number_of_ports_per_computer,number_of_routers,number_of_ports_per_router,search_loop_limit):

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