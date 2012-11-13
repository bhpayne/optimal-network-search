
compute_node_NICs_arry=[
  1,    # computer 0 has 1 empty NIC
  2, # computer 1 has 2 empty NICs
  1,    # computer 2 has 1 empty NIC
  2] # computer 3 has 2 empty NICs
  
print "compute nodes array: "
print compute_node_NICs_arry

fil=open('compute_node_NICs.dat', 'w')
for item in compute_node_NICs_arry:
  fil.write("%s\n" % item)
fil.close()

empty_switch_ports_arry=[
  4, # switch 0 has 4 empty ports 
  4, # switch 1 has 4 empty ports 
  4, # switch 2 has 4 empty ports
  4] # switch 3 has 4 empty ports
  
print "empty switch ports array: "
print empty_switch_ports_arry

fil=open('empty_switch_ports.dat', 'w')
for item in compute_node_NICs_arry:
  fil.write("%s\n" % item)
fil.close()
  
