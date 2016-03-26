#from pyfbsdk import *
import math

def get_k_pos(n_s, n_t):
	return n_s+n_t

def get_k_perc(n_s, n_t):
	return n_s+n_t

def get_k_deg(n_s, n_t):
	return n_s+n_t

def get_k_bet(n_s, n_t):
	return n_s+n_t

def get_k_area(n_s, n_t):
	return n_s+n_t

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

print(get_k(1,2))