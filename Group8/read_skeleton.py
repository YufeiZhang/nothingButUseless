#from pyfbsdk import *
'''
This file is to read all branches of both target and source skeleton
This should be using motion-builder
'''

file_name = "low.txt"
#file_name = "high.txt"

txt = open(file_name).read().split(",")
#print(txt)
#print(len(txt))

branches = []
branch   = []
for i in range(len(txt)):
	branch.append(txt[i][7:])
	if "End" in txt[i]:
		branches.append(branch)
		branch = []
		
print(branches)




