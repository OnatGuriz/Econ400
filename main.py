# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:07:32 2021

@author: cangu
"""
import itertools
import numpy as np

# define the talents and budget
M_1 = 250
M_2 = 250

ar_1 = 1
ar_2 = 1
as_1 = 1
as_2 = 3


movesetSaving1 = [0, 11]
movesetSaving2 = [0, 21]

movesetRecog1 = [0, 12]
movesetRecog2 = [0, 22]

#check for feasibility issues
if all(value >= 0 for value in movesetSaving1) & all(value <= M_1 for value in movesetSaving1):
    print("no problem in agent 1 saving choices")
if all(value >= 0 for value in movesetRecog1) & all(value <= M_1 for value in movesetRecog1):
    print("no problem in agent 1 recognition choices")
if all(value >= 0 for value in movesetSaving2) & all(value <= M_2 for value in movesetSaving2):
    print("no problem in agent 2 saving choices")
if all(value >= 0 for value in movesetRecog2) & all(value <= M_2 for value in movesetRecog2):
    print("no problem in agent 2 recognition choices")

# generate the action space
def genActionSpace(movesetSaving1 , movesetSaving2 , movesetRecog1 , movesetRecog2):
    actionSpace1 = itertools.product(movesetSaving1 , movesetRecog1)
    actionSpace2 = itertools.product(movesetSaving2 , movesetRecog2)
    actionSpace = list(itertools.product(actionSpace1, actionSpace2))
    return actionSpace

#the format of the actionSpace is ((es_1 , er_1) , (es_2 , er_2))

#print(genActionSpace(movesetSaving1 , movesetSaving2 , movesetRecog1 , movesetRecog2))

# computing the output
def prodFunc(es_1, es_2):
    return (es_1 * as_1 + es_2 * as_2)

# computing recognition probabilities
def recogProb(er_1, er_2):
    if (er_1 == 0 and er_2 == 0):
        return ((0.5, 0.5))
    else:
        p1_recog = (ar_1 * er_1) / (ar_1 * er_1 + ar_2 * er_2)
        p2_recog = 1 - p1_recog
        return ((p1_recog, p2_recog))


# computing the estimated utilities
def utilFunc(es_1, er_1, es_2, er_2):
    EU_1 = (recogProb(er_1, er_2)[0] * prodFunc(es_1, es_2)) + (M_1 - es_1 - er_1)
    EU_2 = (recogProb(er_1, er_2)[1] * prodFunc(es_1, es_2)) + (M_2 - es_2 - er_2)
    return EU_1, EU_2
#value[0][] = agent 1 , value [1][] = agent2
#value[][0] = saving , value [][1] = recognition

#All possible actions
Action_SpaceTotal = genActionSpace(movesetSaving1 , movesetSaving2 , movesetRecog1 , movesetRecog2)
value = Action_SpaceTotal[0]

#create a new matrix to compute the expected utilities at every entry
EU_Matrix = Action_SpaceTotal.copy()

#find the expected utility of both agents in every entry
for i in range (0,len(EU_Matrix)):
    value = EU_Matrix[i]
    EU_Matrix[i] = utilFunc(value[0][0] , value[0][1], value[1][0], value[1][1])


#got it from https://stackoverflow.com/questions/3636344/read-flat-list-into-multidimensional-array-matrix-in-python
#maps every possible action into a matrix
col = len(movesetSaving1) * len(movesetRecog1)
ActionMatrixUtil = np.array([EU_Matrix[i:i+col] for i in range (0,len(EU_Matrix), col)])
ActionMatrix = np.array([Action_SpaceTotal[i:i+col] for i in range (0,len(Action_SpaceTotal), col)])

row_num = len(ActionMatrixUtil)
col_num = len(ActionMatrixUtil[0])
print(ActionMatrixUtil[2,0:])
print("break")
print(ActionMatrixUtil[2,0:][0:,1])

#find the maximum of agent 2 utility at every column

#find the maximum of agent 1 utility at every row

np.set_printoptions(precision= 2)
#print(ActionMatrix)


