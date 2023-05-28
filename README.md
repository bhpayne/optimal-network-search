# use

 This script generates random graphs and produces plots of the graph
```bash
python generate_graph.py
```
The parameters for the graph are currently hardcoded
```bash
python generate_graphViz_plot.py
```

Not currently working:
```bash
python fitness_function_all_to_all_hops.py
python fitness_function_bisection_bandwidth.py
python fitness_function_AtoB_hops.py
python make_permutations_to_graph.py
```
# required software

* Python
* GraphViz

Tested on Ubuntu 12.04 64bit

# example output

set the following parameters in "run_search.py"
```
number_of_routers=10
number_of_ports_per_router=10
number_of_computers=10
number_of_ports_per_computer=1
number_of_iterations=1000
```
Sample output:
```
bpayne@bpayne-Alien:~/optimal-network-search$ rm *.png; python run_search.py 
[FN] probably redundant connections are all that is left
[FN] connections:
[[-1, 9], [-4, 3], [-6, 4], [-7, 1], [-5, 2], [-3, 1], [-8, 8], [-10, 6], [-2, 10], [-9, 6], [8, 9], [9, 10], [5, 2], [3, 7], [5, 1], [1, 10], [10, 3], [7, 9], [5, 4], [2, 8], [7, 6], [7, 10], [2, 4], [5, 9], [3, 5], [2, 1], [4, 7], [3, 4], [8, 5], [2, 3], [10, 4], [10, 6], [4, 9], [8, 6], [2, 7], [8, 4], [2, 6], [7, 8], [6, 3], [1, 8], [3, 1], [9, 3], [4, 1], [6, 5], [10, 5], [7, 1], [10, 2], [9, 6], [10, 8], [9, 1], [7, 5], [3, 8], [9, 2], [4, 6]]
[FN] remaining routers:
[5, 7]
remaining empty switch ports:
[5, 7]
initial average hop count is 3.04444444444
new average hop count is 3.0
new average hop count is 2.91111111111
```

The average hop count decreased due to random swaps of connections

# background

The question motivating this project is
"What is the topology of the network which results in the lowest transmission times for an all-to-all communication?"

The parameters are
* number of switches
* number of compute nodes
* number of ports per switch
* number of ports per compute node
Future parameters might be
* physical layout (3D racks and isles of racks)
* message size
* fault tolarance

Obviously a "fully-connected" (each node connects directly to every other node) is optimal, but given fewer ports than the number of nodes this is not possible.

Second-most optimal would be introducing one switch with n ports for n compute nodes. Then each node can communicate to any other node via one hop. However, when n=1,000,000 the switch is not available for purchase. Also, the single switch is a single point of failure.

Thus the optimal network topology depends on real-world factors such as switches available for purchase (should we buy a lots of 24 port switches, or more 1000 port switches), and how many ports should the compute node support?


# task list 

- [ ] write functions to generate other (standard) topologies - 2D mesh, 3D mesh, 2D torus, 3D torus, 6D torus, Dragonfly, Clos
- [ ] compare above listed standard topologies to theoretical scaling predictions and also to analytical predictions for metrics like hop count, bisection bandwidth
- [ ] figure out what actual topologies are at NSF resources -- Ranger, Kraken

Q: does there exist a network topology which performs at least as well as current scientific topologies AND improves all-to-all performance?
ie 
http://networkx.lanl.gov/reference/generated/networkx.generators.geometric.navigable_small_world_graph.html

# other resources

* <http://code.google.com/p/python-graph/>
* <http://www.cs.nmsu.edu/~pfeiffer/classes/573/notes/topology.html>

http://gavinmhackeling.com/blog/2012/10/simulated-annealing-in-python/

http://codecapsule.com/2010/04/06/simulated-annealing-traveling-salesman/

Parallel Simulated Annealing in Python
http://code.google.com/p/parsap/

http://margaretmorgan.com/wesley/python/
http://margaretmorgan.com/wesley/python/anneal.py


Python implementation of algorithms from Russell and Norvig's Artificial Intelligence: A Modern Approach. 
http://code.google.com/p/aima-python/
http://aima-python.googlecode.com/svn/trunk/search.py
