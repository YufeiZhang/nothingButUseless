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

branches = []

if len(skeleton) > 1:
	for i in range(1, len(skeleton)):
		barnch   = []
		barnch.append(skeleton[0]) # ["Hip"]
		current = skeleton[i]
		while len(current) != 1:
			barnch.append(current[0])
			current = current[1]
		barnch.append(current[0])
		print(barnch)
		
			









