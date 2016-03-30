from pyfbsdk import *
import math

'''
This file is to read all branches of both target and source skeleton
This should be using motion-builder
'''

def get_banch(parents, children, index, branches):
	#print(index)
	parents.append(children[0])

	# if there is no children, append this branch to branches
	if len(children) == 1:
		branches.append(parents)
		#print()

	# if there is a children, then go to the child
	elif len(children) == 2:
		parents = get_banch(parents, children[1], index+1, branches)

	# if there are several leaves, then search each leaf
	else:
		for i in range(1,len(children)):
			#print(parents[:index+1])
			#print(children[i])
			new = []
			new = get_banch(parents[:index+1], children[i], index+1, branches)

	return parents


def get_branches(skeleton):
	branches = []
	if len(skeleton) > 1:
		# len(skeleton) maybe can be changed as number of children
		for i in range(1,len(skeleton)): # this is to stop the loop
			branch = []
			branch.append(skeleton[0])

			# initialize the node and get its children
			parents = branch[:len(branch)]
			children = skeleton[i]
			
			# start the loop to find all leaves
			branch = get_banch(parents, children, 1, branches)

			#print()
	#print("\n\n\n\n")
	return branches


if __name__ == "__main__":
	# on motion builder, maybe I just need to get chain_base instead of skeleton
	'''
	The output should be a list of list to store all branckes
	'''
    branches = get_branches(skeleton)
    print(len(branches)) # this tells you how many branches we have
    print(branches)      # this shows all branches in a list







