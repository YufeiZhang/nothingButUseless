import networkx as nx
import numpy as np
import sys
import ast
import sets
import math


def retrieve_skeleton_graph(graphdata):
	""" This function reads a 2-lines file with the node names on line 1 and each 2-node tuple for and edge on line 2. 
		From this data, a NetworkX Graph object is created, and returned.

		Input file format: 
			Nodes: node1,node2,node3
			Edges: node1,node2;node2,node3
	"""

	nodes = graphdata[0].rstrip().split(',')
	edgesList = graphdata[1].rstrip().split(';')

	edges = []
	for e in edgesList:
		edges.append(tuple(e.split(',')))

	graph=nx.Graph()						# Create the graph

	for node in nodes:
		graph.add_node(node)				# Append the nodes

	for edge in edges:
		graph.add_edge(*edge)				# Append the edges


	return graph




def retrieve_coordinates(graphdata):

	coord = graphdata[2].rstrip().split(';')
	coordinates = {}
	for n in coord:
		data = n.split('|') # change ':' when file ready
		name = data[0]
		coord_3d = data[1].split(',')
		coordinates[name] = coord_3d

	return coordinates



def get_max_betweenness(graph):

	nodes = graph.nodes()
	bet = nx.betweenness_centrality(graph)

	m, n = 0, 0
	for i in range(len(nodes)):
		if bet[nodes[i]] > m:
			m = bet[nodes[i]]
			n = i
	root = nodes[n]

	return root




def get_branches(root, graph):

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
			branch = get_branch(parents, children, 1, branches, graph)
	return branches




def get_branch(parents, children, index, branches, graph):

	parents.append(children)

	num_of_path = len(graph.neighbors(children))
	path = graph.neighbors(children)

	# if there is no children, append this branch to branches
	if num_of_path == 1:
		branches.append(parents)

	# if there is a children, then go to the child
	elif num_of_path == 2:
		for i in range(2):
			if path[i] not in parents:
				children = graph.neighbors(children)[i]
				#print children, "<- children"
				parents = get_branch(parents, children, index+1, branches, graph)
	
	# if there are several leaves, then search each leaf
	else:
		for i in range(len(path)):
			if path[i] not in parents:
				new = []

				current_node = graph.neighbors(children)[i]
				# print current_node
				
				new = get_branch(parents[:index+1], current_node, index+1, branches, graph)
	
	return parents




def get_k_pos(s_node, t_node, s_data, t_data):

	for key, value in s_data['position'].iteritems():
		if key == s_node:
			s_coordinates = value
			break

	for key, value in t_data['position'].iteritems():
		if key == t_node:
			t_coordinates = value
			break

	eucli_dist = abs(euclidean_distance(s_coordinates, t_coordinates))
	
	return eucli_dist




def get_k_perc(s_node, t_node, s_branch, t_branch, s_data, t_data):

	def get_coord(node, data):
		return data['position'][node]
		

	def get_node_position_ratio(node, data, branch):
		
		sub_branch_length = 0
		branch_length = 0	
		
		for i in range(1, len(branch)):
			curr_node = branch[i]
			prev_node = branch[i-1]

			curr_coord = get_coord(curr_node, data)
			prev_coord = get_coord(prev_node, data)

			branch_length += euclidean_distance(prev_coord, curr_coord)

			if branch[i] == node:
				sub_branch_length = branch_length

		ratio = sub_branch_length/branch_length 

		return ratio


	# for b in s_branches.iteritems():	# find the right branch
	# 	for n in b_value:
	# 		if n == s_node:
	# 			source_branch = b

	s_node_pos_ratio = get_node_position_ratio(s_node, s_data, s_branch)
	t_node_pos_ratio = get_node_position_ratio(t_node, t_data, t_branch)

	difference = abs(t_node_pos_ratio - s_node_pos_ratio)

	return difference





def euclidean_distance(point_s, point_t):

	delta_x_sq = (float(point_t[0]) - float(point_s[0])) ** 2
	delta_y_sq = (float(point_t[1]) - float(point_s[1])) ** 2
	delta_z_sq = (float(point_t[2]) - float(point_s[2])) ** 2

	eucli_dist = math.sqrt(delta_x_sq + delta_y_sq + delta_z_sq)

	return eucli_dist



def get_k_deg(s_node, t_node, s_data, t_data):

	for key, value in s_data['degree'].iteritems():
		if key == s_node:
			s_betweenness = value
			break

	for key, value in t_data['degree'].iteritems():
		if key == t_node:
			t_betweenness = value
			break

	difference = abs(t_betweenness - s_betweenness)

	return difference
	



def get_k_bet(s_node, s_data):

	for key, value in s_data['betweenness'].iteritems():
		if key == s_node:
			s_betweenness = value
			break

	max_b, min_b = 0, 0
	for key, value in s_data['betweenness'].iteritems():
		if value > max_b:
			max_b = value
		if value < min_b:
			min_b = value


	normalized = abs((s_betweenness - min_b)/(max_b-min_b))

	return normalized





def compute_B_matrix(s_data, t_data, s_branches, t_branches):
	""" Returns a matrix of costs Q for mapping a branch of the source to a branch of the target skeleton.
		Calls compute_branch_mapping_cost() I*J times, i.e. (# of branches in source) * (# of branches in target)

		This method assumes the source skeleton has less nodes than the target skeleton.
		Since in later calculations we need to check for the minimum in each values of the source skeleton, on a 2d matrix 
		we set the columns as the nodes of the source and the rows as the nodes of the target.
		In terms of matrices, the source elements will always be placed as the columns, and the target elements will be the rows.
		Hence the There should always be more rows than columns, in both the cost matrix N and the cost matrix B.

	"""

	def compute_branch_mapping_cost(s_branch, t_branch, s_data, t_data):
		""" Gets the cost of mapping branch s to branch t. (i.e. Q(s_b, t_b))
			Actually no -> It "knows" that a branch must be mapped to a certain other branch, i.e. the function
			checks that the mapping of the two branches has the smallest cost.
			This must be called at every branch comparison.
		"""


		def compute_node_mapping_cost(s_node, t_node, s_branch, t_branch, s_data, t_data):
			""" Computes the cost of mapping a node of branch_s to a node of branch_t. (i.e. K(s_n, t_n))
				This must be called at every node comparison between two branches.
			"""

			# Set the weight coefficients
			a1 = 1.0
			a2 = 2.0
			a3 = 0.2
			a4 = 1.0
			

			# Compute each K
			Kpos = get_k_pos(s_node, t_node, s_data, t_data)
			Kperc = get_k_perc(s_node, t_node, s_branch, t_branch, s_data, t_data)
			Kdeg = get_k_deg(s_node, t_node, s_data, t_data)
			Kbet = get_k_bet(s_node, s_data)


			K = a1*Kpos + a2*Kperc + a3*Kdeg - a4*Kbet
			#print(str(Kpos)+" "+str(Kperc)+" "+str(Kdeg)+" "+str(Kbet))
			return K


		def find_optimal_nodes(costmatrix, s_branches, t_branches):
			""" This function gets the minimal value in each row, 
				i.e. the minimal value for the nodes of the source skeleton to be mapped.
			"""
			costs = []
			mapping = []
			inf = float('inf')

			print(s_branches)
			print(t_branches)
			# print(len(costmatrix))
			# print(len(costmatrix[0]))
			print(costmatrix)
			# print(len(costmatrix)==len(s_branches))
			# print(len(costmatrix[0]) == len(t_branches))

			for i in range(len(costmatrix)):
				min_cost = inf
				src = ''
				dst = ''
				for j in range(len(costmatrix[0])):
					if costmatrix[i][j] < min_cost:
						min_cost = costmatrix[i][j]
						src = s_branches[i]
						dst = t_branches[j]
				mapping.append([src,dst])
				print([src, dst])
				costs.append(min_cost)

			total_cost = sum(costs)
			# print(mapping)
			return mapping, total_cost



		

		# Initialize the N matrix (containing node mapping costs, within a pair of branches)
		inf = float('inf')
		N = [[inf for x in range(len(t_branch))] for x in range(len(s_branch))]

		# Save the cost of mapping a node in the source branch to a node in the target branch, in N
		for i in range(len(s_branch)):
			for j in range(len(t_branch)):
				s_n = s_branch[i]
				t_n = t_branch[j]
				node_cost = compute_node_mapping_cost(s_n, t_n, s_branch, t_branch, s_data, t_data)
				N[i][j] = node_cost


		
		branch_mapping, branch_cost = find_optimal_nodes(N, s_branch, t_branch)

		# Nnp = np.array(N)

		# min_costs = np.amin(Nnp, axis=1)
		# sum_costs = np.sum(min_costs)

		return branch_mapping, branch_cost




	# Initialize the B matrix (containing branch mapping costs), and another containing node pairs mappings
	inf = float('inf')
	B_costs = [[inf for x in range(len(t_branches))] for x in range(len(s_branches))]
	B_mappings = [[[] for x in range(len(t_branches))] for x in range(len(s_branches))]

	# Save the cost of mapping a branch in the source to a branch in the target, in B
	for i in range(len(s_branches)):
		for j in range(len(t_branches)):
			s_b = s_branches[i]
			t_b = t_branches[j]
			branch_mapping, branch_cost = compute_branch_mapping_cost(s_b, t_b, s_data, t_data)
			B_costs[i][j] = branch_cost
			B_mappings[i][j] = branch_mapping 

	B_dict = {'costs':B_costs, 'mappings':B_mappings}

	# Bnp = np.array(B)

	return B_dict



def return_optimal_mapping(costs, mappings):

	best_mapping = []
	inf = float('inf')
	for i in range(len(s_branches)):
		min_cost = inf
		min_maping = []
		for j in range(len(t_branches)):
			if costs[i][j] < min_cost:
				min_cost = costs[i][j]
				min_mapping = mappings[i][j]

		# print(min_mapping)
		# print("\n")
		best_mapping.append(min_mapping)
	
	return best_mapping



def print_best_mapping(mappings):

	for mapping in mappings:
		src = mapping[0]
		dst = mapping[1]
		# print(src)
		# print(dst)
		# print("Source: "+src+" -> Target: "+dst)



if __name__ == "__main__":
	""" Writes in a file a dictionary of dictionary of the form:
			centralities = {"degree" : {"node1":deg1, "node2":deg2},
							"betweenness" : {"node1":bet1, "node2":bet2}}
	
		main: - reads graph data files
		  - creates graphs with networkx
		  - calculates betweenness/degree centralities
		  - get a dictionary of Kpos and Kperc
		  - get the branches in the two skeletons
		  - calculate cost mapping matrix

	"""

	# Retrieve the graph data and create two dictionaries

	filename = "centrality.txt"

	f_source_graph = open("output.txt", 'r')
	f_target_graph = open("outputtarget.txt", 'r')

	source = f_source_graph.read().split('\n')
	target = f_target_graph.read().split('\n')
	
	s_graph = retrieve_skeleton_graph(source)				# Create the graph from the skeleton data provided in a file
	s_deg = nx.degree_centrality(s_graph)					# Compute the degree centrality for each node of the graph and store it as a dictionary
	s_bet = nx.betweenness_centrality(s_graph)				# Compute the betweenness centrality for each node of the graph and store it as a dictionary
	s_pos = retrieve_coordinates(source) 					# Get the dictionary of node coordinates

	t_graph = retrieve_skeleton_graph(target)				# Create the graph from the skeleton data provided in a file
	t_deg = nx.degree_centrality(t_graph)					# Compute the degree centrality for each node of the graph and store it as a dictionary
	t_bet = nx.betweenness_centrality(t_graph)				# Compute the betweenness centrality for each node of the graph and store it as a dictionary
	t_pos = retrieve_coordinates(target) 					# Get the dictionary of node coordinates

	source_data = {'degree':s_deg, 'betweenness':s_bet, 'position':s_pos} # Create the dictionary of centralities
	target_data = {'degree':t_deg, 'betweenness':t_bet, 'position':t_pos} # Create the dictionary of centralities

	

	# Get the branch dictionaries for both graph

	source_root = get_max_betweenness(s_graph)
	target_root = get_max_betweenness(t_graph)

	s_branches = get_branches(source_root, s_graph)
	t_branches = get_branches(target_root, t_graph)

	# print(len(s_branches))
	# print(len(t_branches))

	# print(s_branches)
	# print("-------")
	# print(t_branches)


	# Get the B matrix
	B_dictionary = compute_B_matrix(source_data, target_data, s_branches, t_branches)
	B_costs = B_dictionary['costs']
	B_mappings = B_dictionary['mappings']
	# print(B_mappings)
	optimal_mapping = return_optimal_mapping(B_costs, B_mappings)
	# print(optimal_mapping)
	print_best_mapping(optimal_mapping)


	# print(B)


	# Print the centrality values
	# for key, value in centralities['degree'].iteritems():
	# 	print(key+' '+str(value)) 

	# for key, value in centralities['betweenness'].iteritems():
	# 	print(key+' '+str(value)) 



	# Writing the centrality dictionary to a file (not necessary)
	# outfile = open(filename, 'w')
	# outfile.write(str(centralities))
	# outfile.close()





