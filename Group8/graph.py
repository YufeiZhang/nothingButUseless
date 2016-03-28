import networkx as nx
import sys

def retrieve_skeleton_graph():
	""" This function reads a 2-lines file with the node names on line 1 and each 2-node tuple for and edge on line 2. 
		From this data, a NetworkX Graph object is created, and returned.

		Input file format: 
			Nodes: node1,node2,node3
			Edges: node1,node2;node2,node3
	"""

	inputfile = "output.txt"

	f = open(inputfile, 'r')
	graphFile = f.read().split('\n')		# Read the input file 
	
	nodes = graphFile[0].rstrip().split(',')
	edgesList = graphFile[1].rstrip().split(';')

	edges = []
	for e in edgesList:
		edges.append(tuple(e.split(',')))

	graph=nx.Graph()						# Create the graph

	for node in nodes:
		graph.add_node(node)				# Append the nodes

	for edge in edges:
		graph.add_edge(*edge)				# Append the edges


	return graph




if __name__ == "__main__":
	""" Writes in a file a dictionary of dictionary of the form:
			centralities = {"degree" : {"node1":deg1, "node2":deg2},
							"betweenness" : {"node1":bet1, "node2":bet2}}
	"""



	filename = "centrality.txt"

	graph = retrieve_skeleton_graph()		# Create the graph from the skeleton data provided in a file

	deg = nx.degree_centrality(graph)		# Compute the degree centrality for each node of the graph and store it as a dictionary

	bet = nx.betweenness_centrality(graph)	# Compute the betweenness centrality for each node of the graph and store it as a dictionary


	centralities = {'degree':deg, 'betweenness':bet}

	for key, value in centralities['degree'].iteritems():
		print(key+' '+str(value)) 

	print("--------------")

	for key, value in centralities['betweenness'].iteritems():
		print(key+' '+str(value)) 



	outfile = open(filename, 'w')

	outfile.write(str(centralities))

	outfile.close()
