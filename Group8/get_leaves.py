skeleton = \
['ROOT Hips', \
	['JOINT LHipJoint', \
		['JOINT LeftUpLeg', \
			['JOINT LeftLeg', \
				['JOINT LeftFoot', \
					['JOINT LeftToeBase']]]]], \
	['JOINT RHipJoint', \
		['JOINT RightUpLeg', \
			['JOINT RightLeg', \
				['JOINT RightFoot', \
					['JOINT RightToeBase']]]]], \
	['JOINT LowerBack', \
		['JOINT Spine', \
			['JOINT Spine1', \
				['JOINT Neck', \
					['JOINT Neck1', \
						['JOINT Head']]], \
				['JOINT LeftShoulder', \
					['JOINT LeftArm', \
						['JOINT LeftForeArm', \
							['JOINT LeftHand', \
								['JOINT LeftFingerBase', \
									['JOINT LeftHandIndex1']], \
								['JOINT LThumb']]]]], \
				['JOINT RightShoulder', \
					['JOINT RightArm', \
						['JOINT RightForeArm', \
							['JOINT RightHand', \
								['JOINT RightFingerBase', \
									['JOINT RightHandIndex1']], \
								['JOINT RThumb']]]]] \
			]]]]

#print(skeleton)
# I should get 7 branches


'''
This file need a skeleton in list
Maybe I need anothre file to do read a .bvh file 
and get the output as a python list
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
    branches = get_branches(skeleton)
    print(len(branches)) # this tells you how many branches we have
    print(branches)      # this shows all branches in a list









