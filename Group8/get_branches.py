ny branches we have
#print(branches)     # this shows all branches in a list
#print(branches_posi)
from pyfbsdk import *
import math

'''
This file is to read all branches of both target and source skeleton
This should be using motion-builder

I used People.FBX as a testcase
'''

def get_banch(parents, children, index, branches):
    parents.append(children.Name)

    # if there is no children, append this branch to branches
    if len(children.Children) == 0:
        branches.append(parents)

    # if there is a children, then go to the child
    elif len(children.Children) == 1:
        parents = get_banch(parents, children.Children[0], index+1, branches)

    # if there are several leaves, then search each leaf
    else:
        for i in range(len(children.Children)):
            new = []
            new = get_banch(parents[:index+1], children.Children[i], index+1, branches)
    
    return parents


def get_branches(root):
    branches = []

    if len(root.Children) > 0:
        # you need to check len(root.Children)
        for i in range(len(root.Children)): # this is to stop the loop
            branch = []
            branch.append(root.Name) # skeleton[0] -> root

            # initialize the node and get its children
            parents = branch[:len(branch)]
            children = root.Children[i]
            
            # start the loop to find all leaves
            # the initial index may be wrong, you'd better check it.
            branch = get_banch(parents, children, 1, branches)
            
    return branches


def get_branches_posi(branches, file_name):
    out = open(file_name,"w")
    branches_posi = []
    node = FBVector3d()
    for b in branches:
        bran_posi = []
        for name in b:
            n = FBFindModelByLabelName(name)
            n.GetVector(node, FBModelTransformationType.kModelTranslation)
            bran_posi.append(node)
            
            out.write(repr(node[0]) + " ")
            out.write(repr(node[1]) + " ")
            out.write(repr(node[2]) + '\n')    
        out.write('------------------------------------\n')
        branches_posi.append(bran_posi)
    out.close()
    return branches_posi

# Chose the node that has the highest betweeness
#root = FBFindModelByLabelName('PMD_Kristoff__summer_')
root = FBFindModelByLabelName('Bip01') 
branches = get_branches(root)
branches_posi = get_branches_posi(branches, "1.txt")
print(len(branches)) # this tells you how many branches we have
#print(branches)     # this shows all branches in a list

root2 = FBFindModelByLabelName('PMD_Kristoff__summer_') 
branches2 = get_branches(root2)
branches_posi2 = get_branches_posi(branches2, "2.txt")
print(len(branches2))
