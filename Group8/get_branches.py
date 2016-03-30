from pyfbsdk import *
import math

'''
This file is to read all branches of both target and source skeleton
This should be using motion-builder
'''

def get_banch(parents, children, index, branches):
	print(index)
	#marker = FBFindModelByLabelName('Marker01')
	#m_pos = FBVector3d() marker.GetVector(m_pos,FBModelTransformationType.kModelTranslation)
	parents.append(children.Name)

	# if there is no children, append this branch to branches
	if len(children.Children) == 1:
		branches.append(parents)
		print()

	# if there is a children, then go to the child
	elif len(children.Children) == 2:
		parents = get_banch(parents, children.Children[0], index+1, branches)

	# if there are several leaves, then search each leaf
	else:
		for i in range(len(children.Children)):
			#print(parents[:index+1])
			#print(children[i])
			new = []
			new = get_banch(parents[:index+1], children.Children[i], index+1, branches)
	#target_rot = FBVector3d(0,90,0)
	return parents


# all I need is just a root node
# parentNode = node.Parent
# childCount = len(node.Children)
# firstChild = node.Children[0]
def get_branches(root):
	branches = []
	print(root)
	print(root.Name)

	if len(root.Children) > 1:
		# you need to check len(root.Children)
		for i in range(root.Children): # this is to stop the loop
			branch = []
			branch.append(root.Name) # skeleton[0] -> root

			# initialize the node and get its children
			parents = branch[:len(branch)]
			children = root.Children[i]
			
			# start the loop to find all leaves
			# the initial index may be wrong, you'd better check it.
			branch = get_banch(parents, children, 1, branches)

			#print()
	#print("\n\n\n\n")

	return branches


if __name__ == "__main__":
	# Chose the node that has the highest betweeness
	root = FBFindModelByLabelName('JOINT Spine1') 
	#branches = []
    branches = get_branches(root)
    print(len(branches)) # this tells you how many branches we have
    print(branches)      # this shows all branches in a list









