#from pyfbsdk import *
from math import sqrt
s_s = [[[0,0,0],[0,3,0],[0,6,0],[0,9,0],[0,12,0]],     \
	   [[0,0,0],[0,-3,0],[0,-6,0],[0,-9,0],[0,-12,0]], \
	   [[0,0,0],[0,3,2],[0,6,2],[0,9,2],[0,12,2]],     \
	   [[0,0,0],[0,0,-2],[0,0,-4],[0,0,-6]],           \
	   [[0,0,0],[0,0,2],[0,0,4],[0,0,5]] 
]

s_t = [[[0,0,0],[0,4,0],[0,8,0],[0,12,0]],             \
	   [[0,0,0],[0,0,-2],[0,0,-4],[0,0,-6]]
]

name_s = ["l_arm", "r_arm", "l_wing", "back", "head"]
name_t = ["l_arm", "back"]

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
def get_k_perc(length_n_s, length_n_t, length_b_a, length_b_h):
	return abs(length_n_t/length_b_h - length_n_s/length_b_a)

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
	length_b_a = 0
	length_b_h = 0

	# get the lengh of branch a
	for i in range(1,len(b_a)):
		d_x_a = b_a[i][0] - b_a[i-1][0]
		d_y_a = b_a[i][1] - b_a[i-1][1]
		d_z_a = b_a[i][2] - b_a[i-1][2]
		length_b_a += sqrt(d_x_a**2 + d_y_a**2 + d_z_a**2)

	# get the length of branch h
	for i in range(1,len(b_h)):
		d_x_h = b_h[i][0] - b_h[i-1][0]
		d_y_h = b_h[i][1] - b_h[i-1][1]
		d_z_h = b_h[i][2] - b_h[i-1][2]
		length_b_h += sqrt(d_x_h**2 + d_y_h**2 + d_z_h**2)

	length_n_s = 0
	cost_map = [[0 for x in range(len(b_h)-1)] for x in range(len(b_a)-1)] 
	for i in range(len(cost_map)):
		length_n_t = 0

		# get length_n_s 
		d_x_a = b_a[i+1][0] - b_a[i][0]
		d_y_a = b_a[i+1][1] - b_a[i][1]
		d_z_a = b_a[i+1][2] - b_a[i][2]
		length_n_s += sqrt(d_x_a**2 + d_y_a**2 + d_z_a**2)
		
		for j in range(len(cost_map[0])):
			# get length_n_t
			d_x_h = b_h[j+1][0] - b_h[j][0]
			d_y_h = b_h[j+1][1] - b_h[j][1]
			d_z_h = b_h[j+1][2] - b_h[j][2]
			length_n_t += sqrt(d_x_h**2 + d_y_h**2 + d_z_h**2)

			cost_map[i][j] = get_k(b_a, b_h, i, j, length_b_a, length_b_h, length_n_s, length_n_t)
	return cost_map

def get_cost_sum(cost_map):
	cost_sum = 0
	for i in range(len(cost_map)):
		cost_sum += min(cost_map[i])
	return cost_sum

def get_q_matrix(s_s, s_t):
	q_matrix = [[0 for x in range(len(s_s))] for x in range(len(s_t))]
	for i in range(len(s_t)):
		b_h = s_t[i]
		for j in range(len(s_s)):
			b_a = s_s[j]
			cost_map = get_mapping_cost(b_a, b_h)
			# cost_map is also how we need to retarget
			# print(cost_map) 
			q_matrix[i][j] = get_cost_sum(cost_map)
	return q_matrix


# __init__
q_matrix = get_q_matrix(s_s, s_t)

for i in range(len(q_matrix)):
	num = q_matrix[i].index(min(q_matrix[i]))
	print("source =", name_s[num], " -> ", name_t[i])






