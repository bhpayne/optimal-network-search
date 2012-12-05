# network graph input/output module
import pickle # serialize data output
# import cPickle as pickle # "upto 1000 times faster because it is in C"

def writeGraphToFile(number_of_switches,number_of_computers,connections):
  output=open('graph.pkl','wb')
  pickle.dump(number_of_switches,output)
  pickle.dump(number_of_computers,output)
  pickle.dump(connections,output)
  output.close()

def readGraphFromFile():
  pkl_file=open('graph.pkl','rb') # read
  number_of_switches=pickle.load(pkl_file)
  number_of_computers=pickle.load(pkl_file)
  connections=pickle.load(pkl_file)
  pkl_file.close()
  return number_of_switches,number_of_computers,connections
