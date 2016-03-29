from pyfbsdk import *
import math

'''
This file is to read all branches of both target and source skeleton
This should be using motion-builder
'''

def get_branches(skeleton):
    branches, branch, node = [], [], FBVector3d()
    
    # get the node point and store it in 'node'
    goal.GetVector( node, FBModelTransformationType.kModelTranslation)

    # finde the lastNode -> chain_bace.Chidren[0].Chileren[0] ...
    # and find how many bones are there in total
    lastNode = chain_base.Children[0]
    numOfBones = 1
    while len(lastNode.Children) == 1:
        lastNode = lastNode.Children[0]
        numOfBones += 1
          
    # If the distance > thresh or iteration < numOfBones * 10 -> countinue
    while getDist(pn, t) > thresh and iteration < 10*numOfBones:
        # refresh the screen a the bigining
        FBSystem().Scene.Evaluate()

        # get the latest position of the lastNode and store it to 'pn'
        lastNode.GetVector(pn, FBModelTransformationType.kModelTranslation)
        
        # if current point does not have a parent, set lastNode as chain_base
        if chain_base.Parent == None:  
            chain_base = lastNode

        # get the parent of the chain_base
        # chain_base.Parent is the rotation center
        chain_base = chain_base.Parent
        chain_base.GetVector(pm,FBModelTransformationType.kModelTranslation)
     
        # get vector1, vector2, and align_matrix as is told in slides
        vector1 = pn - pm
        vector2 = t  - pm
        R = align_matrix(vector1,vector2)

        # This is copied from the sides, marker is the rotation center        
        marker = chain_base 
        cur_Ori = FBMatrix() 
        marker.GetMatrix(cur_Ori,FBModelTransformationType.kModelRotation,False) 

        # This is copied from the sides donig the rotation
        final_Ori = R * cur_Ori 
        ori_vec = FBVector3d() 
        FBMatrixToRotation(ori_vec,final_Ori) 
        marker.Rotation = ori_vec

        iteration+=1


#chain_base = FBFindModelByLabelName('Node')







