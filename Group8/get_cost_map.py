#from pyfbsdk import *
from math import sqrt
# the input need to be a list of list of list
# [0,0,0] -> the position of a node
# [[0,0,0],[0,3,0],[0,6,0],[0,9,0],[0,12,0]] -> positions of nodes in a branch
# s_s -> a list contains all branches
s_s = [[[0,0,0],[0,3,0],[0,6,0],[0,9,0],[0,12,0]],     \
	   [[0,0,0],[0,-3,0],[0,-6,0],[0,-9,0],[0,-12,0]], \
	   [[0,0,0],[0,3,2],[0,6,2],[0,9,2],[0,12,2]],     \
	   [[0,0,0],[0,0,-2],[0,0,-4],[0,0,-6]],           \
	   [[0,0,0],[0,0,2],[0,0,4],[0,0,5]] 
]

s_t = [[[0,0,0],[0,4,0],[0,8,0],[0,12,0]],             \
	   [[0,0,0],[0,-4,0],[0,-8,0],[0,-12,0]],          \
	   [[0,0,0],[0,0,-1.5],[0,0,-3],[0,0,-4.5]],       \
	   [[0,0,0],[0,0,0.15],[0,0,3],[0,0,3.8]] 
]

# this is only for testing, it store all the names of branches
name_s = ["s_l_arm", "s_r_arm", "s_l_wing", "s_back", "s_head"]
name_t = ["t_l_arm", "t_r_arm", "t_back", "t_head"]


# the positional difference (Euclidean distance) between the two nodes
def get_k_pos(n_s, n_t, r_s, r_h):
	delta_x_sq = (n_t[0] - n_s[0]) ** 2
	delta_y_sq = (n_t[1] - n_s[1]) ** 2
	delta_z_sq = (n_t[2] - n_s[2]) ** 2
	eucli_dist = sqrt(delta_x_sq + delta_y_sq + delta_z_sq)
	return eucli_dist
	#return 0


# the difference of the nodes’ position along their individual branches 
# given in percentage of the complete branch length
# length from a node to root / length of a branch
def get_k_perc(length_n_s, length_n_t, length_b_a, length_b_h):
	return abs(length_n_t/length_b_h - length_n_s/length_b_a)

# the difference of the nodes’ degree centrality
# You can ignore the inputs, I will get this value from Maxim's output
def get_k_deg(n_s, n_t, r_s, r_h):
	return 0

# normalized betweenness-centrality in the high-resolution tree
# You can ignore the inputs, I will get this value from Maxim's output
def get_k_bet(n_s, n_t, r_s, r_h):
	return 0

# normalized area of the node in the high-resolution tree
# You can ignore the inputs, I will get this value from Maxim's output
def get_k_area(n_s, n_t, r_s, r_h):
	return 0

# cost K(Nsh, Nta) of assigning two node
# b_a -> source branch
# b_h -> target branch
# i,j -> index of branch of source and target branches respectively
# length_b_a -> length of source branch
# length_b_h -> length of target branch
# length_n_s -> length of source node from source root
# length_n_t -> length of target node from target root
def get_k(b_a, b_h, i, j, length_b_a, length_b_h, length_n_s, length_n_t):
	α1 = 10.0
	α2 = 2.0
	α3 = 0.2
	α4 = 1.0
	α5 = 0.5
	value = α1 * get_k_pos (b_a[i], b_h[j],    b_a[ 0],    b_h[ 0]) + \
			α2 * get_k_perc(length_n_s, length_n_t, length_b_a, length_b_h) + \
			α3 * get_k_deg (b_a[i], b_h[j],    b_a[ 0],    b_h[ 0]) + \
			α4 * get_k_bet (b_a[i], b_h[j],    b_a[ 0],    b_h[ 0]) + \
			α5 * get_k_area(b_a[i], b_h[j],    b_a[ 0],    b_h[ 0])
	return value


# get the cost of mapping
def get_mapping_cost(b_a, b_h):
	# length_b_a -> length of source branch
	# length_b_h -> length of target branch
	length_b_a = 0
	length_b_h = 0

	# get the lengh of source branch which is used to calculate k_perc
	for i in range(1,len(b_a)):
		d_x_a = b_a[i][0] - b_a[i-1][0]
		d_y_a = b_a[i][1] - b_a[i-1][1]
		d_z_a = b_a[i][2] - b_a[i-1][2]
		length_b_a += sqrt(d_x_a**2 + d_y_a**2 + d_z_a**2)

	# get the length of target branch which is used to calculate k_perc
	for i in range(1,len(b_h)):
		d_x_h = b_h[i][0] - b_h[i-1][0]
		d_y_h = b_h[i][1] - b_h[i-1][1]
		d_z_h = b_h[i][2] - b_h[i-1][2]
		length_b_h += sqrt(d_x_h**2 + d_y_h**2 + d_z_h**2)

	length_n_s = 0
	cost_map = [[0 for x in range(len(b_h)-1)] for x in range(len(b_a)-1)] 
	for i in range(len(cost_map)):
		length_n_t = 0

		# get length_n_s which is used to calculate k_perc
		d_x_a = b_a[i+1][0] - b_a[i][0]
		d_y_a = b_a[i+1][1] - b_a[i][1]
		d_z_a = b_a[i+1][2] - b_a[i][2]
		length_n_s += sqrt(d_x_a**2 + d_y_a**2 + d_z_a**2)
		
		for j in range(len(cost_map[0])):
			# get length_n_t which is used to calculate k_perc
			d_x_h = b_h[j+1][0] - b_h[j][0]
			d_y_h = b_h[j+1][1] - b_h[j][1]
			d_z_h = b_h[j+1][2] - b_h[j][2]
			length_n_t += sqrt(d_x_h**2 + d_y_h**2 + d_z_h**2)

			cost_map[i][j] = get_k(b_a, b_h, i, j, length_b_a, length_b_h, length_n_s, length_n_t)
	return cost_map


# calculate the sum of K
def get_cost_sum(cost_map):
	cost_sum = 0
	for i in range(len(cost_map)):
		cost_sum += min(cost_map[i])
	return cost_sum

def get_q_matrix(s_s, s_t):
	q_matrix = [[0 for x in range(len(s_t))] for x in range(len(s_s))]
	for i in range(len(s_s)): # for each branch in source
		b_a = s_s[i] 
		for j in range(len(s_t)): # for each branch in target
			b_h = s_t[j]

			# calculate cost_map, which is node mapping cost K
			# it is a list of list storing the cost mapping from each
			# source node to each target node
			cost_map = get_mapping_cost(b_a, b_h)

			# q matrix[i][j] is the sum of node mapping cost K
			q_matrix[i][j] = get_cost_sum(cost_map)
	return q_matrix

# __init__
# s_s: a list that contains the position of source nodes in a branch
# s_t: a list that contains the position of target nodes in a branch
# q_matrix stored the cost to map each source branch to each target branch
q_matrix = get_q_matrix(s_s, s_t)


for i in range(len(q_matrix)):
	# num is the index of least cost mapping one branch to a target branch
	num = q_matrix[i].index(min(q_matrix[i]))
	print("source:", name_s[i]," -> target:", name_t[num])

	b_a = s_s[i]
	b_h = s_t[num]
	cost_map = [[0 for x in range(len(b_a)-1)] for x in range(len(b_h)-1)] 
	cost_map = get_mapping_cost(b_a, b_h)
	for j in range(len(cost_map)):
		print("we need to retarget", j+1, "th node from source onto", cost_map[j].index(min(cost_map[j]))+1, "of target")
	print(cost_map)
	print()


