import lib_network_optimization as nopt

#************ MAIN BODY *********************

# for bisection halting:
confidence_of_finding_minimum_bisection=1
max_picks=1000
#filename="test_network_ALLTOALL_8routers_8computers.input"
#filename="test_network_ONE_ROUTER_1router_8computers.input"
#filename="test_network_ASYMMETRIC_PAIR_2routers_8_computers.input"
filename="test_network_ALLTOALL_8routers_8computers.input"
#filename="test_network_SYMMETRIC_PAIR_2routers_8computers.input"
#filename="test_network_SYMMETRIC_SQUARE_4routers_8computers.input"
#filename="test_network_SYMMETRIC_CENTIPEDE_4routers_8computers.input"

try: 
  number_of_routers,number_of_computers,connections = nopt.translateTestNetworkFromFileToGraph(filename)
except IndexError:
  print("ERROR: probably extra lines in "+filename)
  exit()
  
nopt.draw_computer_and_router_graph_pictures(connections,"specified")

try:
  hop_count_distribution=nopt.fitness_function_find_all_compute_hop_lengths(number_of_computers,connections)
except nx.NetworkXNoPath:
  print("ERROR: initial network is segmented. Fix the random network generation algorithm")
  exit()
  
average_hop_count=float(sum(hop_count_distribution))/len(hop_count_distribution) # average hop count
print("average hop count: "+str(average_hop_count))

#number_of_picks=nopt.how_many_picks_computers_routers(confidence_of_finding_minimum_bisection,number_of_computers,number_of_routers,max_picks)
number_of_picks=1000
best_bisection_count=10000
number_of_permutations=1000
weight_error=0.1
bisection_array=[]
for bcount in range(number_of_picks):
  bisection_count,left_partition,right_partition=nopt.fitness_function_bisection_count_computers_and_routers(number_of_computers,number_of_routers,connections,number_of_permutations,weight_error)
  bisection_array.append(bisection_count)
  if (bisection_count<best_bisection_count):
    best_left=left_partition
    best_right=right_partition
    best_bisection_count=bisection_count

print ("minimum bisection found: "+str(min(bisection_array)))
print ("left  partition of routers and their weights: "+str(best_left))
print ("right partition of routers and their weights: "+str(best_right))

hist={}
for x in bisection_array: hist[x] = hist.pop(x,0)+1
print hist