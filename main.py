# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:07:32 2021

@author: cangu
"""
import itertools
import numpy as np
import pandas as pd

# define the talents and budget
M_1 = 400
M_2 = 400

ar_1 = 1
ar_2 = 1
as_1 = 3
as_2 = 3


movesetSaving1 = [0, 100]
movesetSaving2 = [0, 200]

movesetRecog1 = [0, 100]
movesetRecog2 = [0, 200]

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
    actionSpace1 = tuple(itertools.product(movesetSaving1 , movesetRecog1))
    actionSpace2 = tuple(itertools.product(movesetSaving2 , movesetRecog2))
    actionSpace = tuple(itertools.product(actionSpace1, actionSpace2))
    return actionSpace1,actionSpace2,actionSpace
""" this function returns 
all possible actions of 1 at entry 0
all possible actions of 2 at enry 1
all jointly possible actions at entry 2
"""


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


# computing the estimated utilities with 2 decimals
def utilFunc(es_1, er_1, es_2, er_2):
    EU_1 = round((recogProb(er_1, er_2)[0] * prodFunc(es_1, es_2)) + (M_1 - es_1 - er_1),2)
    EU_2 = round((recogProb(er_1, er_2)[1] * prodFunc(es_1, es_2)) + (M_2 - es_2 - er_2),2)
    return EU_1, EU_2

#value[0][] = agent 1 , value [1][] = agent2
#value[][0] = saving , value [][1] = recognition

#All possible actions mapped to a dataframe
Action_SpaceTotal = genActionSpace(movesetSaving1 , movesetSaving2 , movesetRecog1 , movesetRecog2)
Action_SpaceTotal_df = pd.DataFrame(Action_SpaceTotal[2])

colnames = Action_SpaceTotal[0]
rownames= Action_SpaceTotal[1]


#row and columns for reference
print("colnames: " + str(colnames))
print("rownames: " + str(rownames))


#Here we set the row names and column names first
ActionFrame_df = pd.DataFrame(columns= colnames, index = rownames)
#then we assign their respective values
#bu donguyu kurana kadar omrum bitti
for i in range(0, len(rownames)):
    for j in range(0, len(colnames)):
        ActionFrame_df.iloc[j,i] = tuple((colnames[i]+rownames[j]))


"""" Format of the Dataframes
     Top : I^1_s , I^1_r
     Left: I^2_s , I^2_r
     Payoffs : (EU_1 , EU_2)
 """
#now we will compute all possible utilites on the action space dataframe to get utilities
UtilityFrame_df = ActionFrame_df.copy()

for i in range(0, len(rownames)):
    for j in range(0, len(colnames)):
        value = UtilityFrame_df.iloc[i, j]
        UtilityFrame_df.iloc[i,j] = utilFunc(value[0], value[1], value[2], value[3])


