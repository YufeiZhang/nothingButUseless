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

	#print graph.nodes()
	#print graph.edges()
	return graph


def get_banch(parents, children, index, branches):
	parents.append(children)

	num_of_path = len(graph.neighbors(children))
	path = graph.neighbors(children)
	#print index

	# if there is no children, append this branch to branches
	if num_of_path == 1:
		branches.append(parents)
		print parents
		print "\n"

	# if there is a children, then go to the child
	elif num_of_path == 2:
		for i in range(2):
			#print path[i], "<- path", i
			#print parents, "<- parents"
			if path[i] not in parents:
				children = graph.neighbors(children)[i]
				#print children, "<- children"
				parents = get_banch(parents, children, index+1, branches)
	
	# if there are several leaves, then search each leaf
	else:
		print "\n-------------------------------------"
		print path

		for i in range(len(path)):
			if path[i] not in parents:
				new = []

				current_node = graph.neighbors(children)[i]
				print current_node
				
				new = get_banch(parents[:index+1], current_node, index+1, branches)
	return parents


def get_branches(root):
	branches = []
	if len(graph.neighbors(root)) > 1:
		for i in range(len(graph.neighbors(root))): # this is to stop the loop
			branch = []
			branch.append(root)

			# initialize the node and get its children
			parents = branch[:len(branch)]
			children = graph.neighbors(root)[i]
			#print children
			
			# start the loop to find all leaves
			branch = get_banch(parents, children, 1, branches)
	return branches


if __name__ == "__main__":
	""" Writes in a file a dictionary of dictionary of the form:
			centralities = {"degree" : {"node1":deg1, "node2":deg2},
							"betweenness" : {"node1":bet1, "node2":bet2}}
	"""



	filename = "centrality.txt"

	graph = retrieve_skeleton_graph()		# Create the graph from the skeleton data provided in a file

	nodes = graph.nodes()
	edges = graph.edges()

	#deg = nx.degree_centrality(graph)		# Compute the degree centrality for each node of the graph and store it as a dictionary

	bet = nx.betweenness_centrality(graph)	# Compute the betweenness centrality for each node of the graph and store it as a dictionary
	
	# finding the highest bet and set it as root
	m, n = 0, 0
	for i in range(len(nodes)):
		if bet[nodes[i]] > m:
			m = bet[nodes[i]]
			n = i
	root = nodes[n]

	branches = get_branches(root)

	print(len(branches))



	
