#!/usr/bin/python

# Ben Payne
# bpayne@lps.umd.edu

# purpose: measure bisection bandwidth of network

# output: 

import lib_network_optimization as nopt # Ben's module

nopt.fitness_function_bisection_count(number_of_computers,number_of_routers,connections)

number_of_switches,number_of_computers,connections=nopt.readGraphFromFile()