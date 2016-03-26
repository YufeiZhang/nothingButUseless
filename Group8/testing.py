#from pyfbsdk import *
from math import sqrt

# the positional difference (Euclidean distance) between the two nodes
def get_k_pos(n_s, n_t):
	delta_x_sq = (n_t[0] - n_s[0]) ** 2
	delta_y_sq = (n_t[1] - n_s[1]) ** 2
	delta_z_sq = (n_t[2] - n_s[2]) ** 2
	return sqrt(delta_x_sq + delta_y_sq + delta_z_sq)

# the difference of the nodes’ position along their individual branches 
# given in percentage of the complete branch length
def get_k_perc(n_s, n_t):
	return n_s[0]+n_t[0]

# the difference of the nodes’ degree centrality
def get_k_deg(n_s, n_t):
	return n_s[0]+n_t[0]

# normalized betweenness-centrality in the high-resolution tree
def get_k_bet(n_s, n_t):
	return n_s[0]+n_t[0]

# normalized area of the node in the high-resolution tree
def get_k_area(n_s, n_t):
	return n_s[0]+n_t[0]

# cost K(Nsh, Nta) of assigning two node
def get_k(n_s, n_t):
	α1 = 10.0
	α2 = 2.0
	α3 = 0.2
	α4 = 1.0
	α5 = 0.5
	value = α1 * get_k_pos(n_s, n_t)  + \
			α2 * get_k_perc(n_s, n_t) + \
			α3 * get_k_deg(n_s, n_t)  + \
			α4 * get_k_bet(n_s, n_t)  + \
			α5 * get_k_area(n_s, n_t)
	return value

# get the cost of mapping
def get_mapping_cost(b_a, b_h):
	for i in range(len(b_a)):
		for j in range(len(b_h)):
			cost_map[i][j] = get_k(b_a[i], b_h[j])
	return cost_map


print(get_k([0,0,0],[1,1,1]))