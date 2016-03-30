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

def get_banch(parents, children, index, branches):
	print(index)
	if len(children) == 1:
		parents.append(children[0])
		branches.append(parents)
		print()

	elif len(children) == 2:
		parents.append(children[0])
		parents = get_banch(parents, children[1], index+1, branches)

	else:
		parents.append(children[0])
		for i in range(1,len(children)):
			print(parents[:index+1])
			print(children[i])
			new = []
			new = get_banch(parents, children[i], index, branches)
			
	return parents

def get_branches(skeleton):
	branches = []
	if len(skeleton) > 1:
		for i in range(1,len(skeleton)): # this is to stop the loop
			branch = []
			branch.append(skeleton[0])

			parents = branch[:len(branch)]
			children = skeleton[i]
			
			# ---------------------- add code here ----------------------

			branch = get_banch(parents, children, 1, branches)

			# ---------------------- add code end ----------------------
			
			#print(branch)
			print()


	return branches
	




if __name__ == "__main__":
    get_branches(skeleton)









