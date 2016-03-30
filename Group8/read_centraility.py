#from pyfbsdk import *
'''
This file is to read centrality
'''

file_name = "centrality.txt"
txt = open(file_name).read().split("\n")
#print(txt)
#print(txt)

branches = []
branch   = []
ok_list = ["ROOT","JOINT","END"]
length = len(txt)

for i in range(length):
	#print(txt[length-i-1])
	if  "ROOT"  in txt[i] or "JOINT" in txt[i] or "END"   in txt[i]:
		print(txt[i])
		#node_name = txt[i].split(" ")[1])

		
