#from pyfbsdk import *
from math import sqrt

b_a = [[0,0,0],[0,3,0],[0,6,0],[0,9,0],[0,12,0]]
#b_a = [[0,0,0],[0,2,0],[0,4,0],[0,6,0]]


b_h = [[0,0,0],[0,4,0],[0,8,0],[0,12,0]]

# the positional difference (Euclidean distance) between the two nodes
def get_k_pos(n_s, n_t, r_s, r_h):
	delta_x_sq = (n_t[0] - n_s[0]) ** 2
	delta_y_sq = (n_t[1] - n_s[1]) ** 2
	delta_z_sq = (n_t[2] - n_s[2]) ** 2
	return sqrt(delta_x_sq + delta_y_sq + delta_z_sq)

# the difference of the nodes’ position along their individual branches 
# given in percentage of the complete branch length
def get_k_perc(n_s, n_t, end_s, end_h):

	return n_s[0]+n_t[0]

# the difference of the nodes’ degree centrality
def get_k_deg(n_s, n_t, r_s, r_h):
	return 0

# normalized betweenness-centrality in the high-resolution tree
def get_k_bet(n_s, n_t, r_s, r_h):
	return 0

# normalized area of the node in the high-resolution tree
def get_k_area(n_s, n_t, r_s, r_h):
	return 0

# cost K(Nsh, Nta) of assigning two node
def get_k(b_a, b_h, i, j):
	α1 = 10.0
	α2 = 2.0
	α3 = 0.2
	α4 = 1.0
	α5 = 0.5
	value = α1 * get_k_pos (b_a[i], b_h[j], b_a[ 0], b_h[ 0]) + \
			α2 * get_k_perc(b_a[i], b_h[j], b_a[-1], b_h[-1]) + \
			α3 * get_k_deg (b_a[i], b_h[j], b_a[ 0], b_h[ 0]) + \
			α4 * get_k_bet (b_a[i], b_h[j], b_a[ 0], b_h[ 0]) + \
			α5 * get_k_area(b_a[i], b_h[j], b_a[ 0], b_h[ 0])
	return value

# get the cost of mapping
def get_mapping_cost(b_a, b_h):
	length_b_a = 0
	length_b_h = 0

	# get the lengh of branch a
	for i in range(1,len(b_a)):
		d_x_a = b_a[i][0] - b_a[i-1][0]
		d_y_a = b_a[i][1] - b_a[i-1][1]
		d_z_a = b_a[i][2] - b_a[i-1][2]
		length_b_a += sqrt(d_x_a**2 + d_y_a**2 + d_z_a**2)
	print (length_b_a)

	# get the length of branch h
	for i in range(1,len(b_h)):
		d_x_h = b_h[i][0] - b_h[i-1][0]
		d_y_h = b_h[i][1] - b_h[i-1][1]
		d_z_h = b_h[i][2] - b_h[i-1][2]
		length_b_h += sqrt(d_x_h**2 + d_y_h**2 + d_z_h**2)
	print (length_b_h)

	cost_map = [[0 for x in range(len(b_h)-1)] for x in range(len(b_a)-1)] 
	for i in range(len(cost_map)):
		for j in range(len(cost_map[0])):
			cost_map[i][j] = get_k(b_a, b_h, i, j)
	return cost_map


print(get_mapping_cost(b_a, b_h))