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

gametype = "NT"

movesetSaving1 = [0, 100, 200]
movesetSaving2 = [0, 100, 200]

movesetRecog1 = [0, 100, 200]
movesetRecog2 = [0, 100, 200]

moveset_1 = [0 , 100]
moveset_2 = [0, 200]



# generate the action space for non-transfer games
def genActionSpace_NT(movesetSaving1, movesetSaving2, movesetRecog1, movesetRecog2):
    actionSpace1 = tuple(itertools.product(movesetSaving1, movesetRecog1))
    actionSpace2 = tuple(itertools.product(movesetSaving2, movesetRecog2))
    return actionSpace1, actionSpace2


def genActionSpace_T(moveset_1 , moveset_2):
    movesetRecog1_T = []
    movesetRecog2_T = []
    movesetSaving1_T = moveset_1
    movesetSaving2_T = moveset_2
    for i in range (0,len(moveset_1)):
        movesetRecog1_T.append(M_1 - moveset_1[i])
    for i in range (0,len(moveset_2)):
        movesetRecog2_T.append(M_2 - moveset_2[i])
    actionSpace1 = list(itertools.product(movesetSaving1_T, movesetRecog1_T))
    actionSpace2 = list(itertools.product(movesetSaving2_T, movesetRecog2_T))
    actionSpace1 = list(filter(lambda x: x[0]+x[1] <= M_1 , actionSpace1))
    actionSpace2 = list(filter(lambda x: x[0] + x[1] <= M_2, actionSpace2))
    return actionSpace1, actionSpace2

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
    EU_1 = round((recogProb(er_1, er_2)[0] * prodFunc(es_1, es_2)) + (M_1 - es_1 - er_1), 2)
    EU_2 = round((recogProb(er_1, er_2)[1] * prodFunc(es_1, es_2)) + (M_2 - es_2 - er_2), 2)
    return EU_1, EU_2


# value[0][] = agent 1 , value [1][] = agent2
# value[][0] = saving , value [][1] = recognition

# All possible actions mapped to a dataframe
if(gametype == "NT"):
    Action_SpaceTotal = genActionSpace_NT(movesetSaving1, movesetSaving2, movesetRecog1, movesetRecog2)
elif(gametype == "T"):
    Action_SpaceTotal = genActionSpace_T(moveset_1, moveset_2)
else:
    print("choose a valid game")

colnames = Action_SpaceTotal[0]
rownames = Action_SpaceTotal[1]

colnames_str=[]
rownames_str=[]

for i in range (0,len(colnames)):
    colnames_str.append(str(colnames[i])) 

for j in range (0, len(rownames)):
    rownames_str.append(str(rownames[j]))


# row and columns for reference
#print("colnames: " + str(colnames))
#print("rownames: " + str(rownames))

# Here we set the row names and column names first
ActionFrame_df = pd.DataFrame(columns= colnames_str, index= rownames_str)
# then we assign their respective values
# bu donguyu kurana kadar omrum bitti
for i in range(0, len(rownames)):
    for j in range(0, len(colnames)):
        ActionFrame_df.iloc[j, i] = tuple((colnames[i] + rownames[j]))

"""" Format of the Dataframes
     Top : I^1_s , I^1_r
     Left: I^2_s , I^2_r
     Payoffs : (EU_1 , EU_2)
 """
# now we will compute all possible utilites on the action space dataframe to get utilities and we will create a reversed one for ease of computation
UtilityFrame1_df = ActionFrame_df.copy()
UtilityFrame2_df = ActionFrame_df.copy()
UtilityFrameTotal_df = ActionFrame_df.copy()

for i in range(0, len(rownames)):
    for j in range(0, len(colnames)):
        value = UtilityFrame1_df.iloc[i, j]
        UtilityFrame1_df.iloc[i, j] = utilFunc(value[0], value[1], value[2], value[3])[0]
        UtilityFrame2_df.iloc[i,j] = utilFunc(value[0], value[1], value[2] , value[3])[1]
        UtilityFrameTotal_df.iloc[i,j] =  utilFunc(value[0], value[1], value[2] , value[3])
UtilityFrame1_df = UtilityFrame1_df.astype(float)
UtilityFrame2_df = UtilityFrame2_df.astype(float)

#taken from https://www.geeksforgeeks.org/python-intersection-two-lists/?ref=lbp
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

#finds the NE the main problem is idxmax() returns onyl the first row if there is a tie
#this is problematic since it might lead to it not finding any NE

def findNE(Payoff_1 , Payoff_2):
    BR_1 = list(zip(Payoff_1.idxmax(axis = 1).to_numpy(),Payoff_1.idxmax(axis = 1).index.to_numpy()))
    BR_2 = list(zip(Payoff_2.idxmax(axis = 0).index.to_numpy(),Payoff_2.idxmax(axis = 0).to_numpy()))
    NE = intersection(BR_1 , BR_2)
    return NE

print("The Nash Equilibrium is " + str((findNE(UtilityFrame1_df , UtilityFrame2_df))))



"""
print(UtilityFrame1_df.idxmax(axis = 1).to_numpy())
print(UtilityFrame1_df.idxmax(axis = 1).index.to_numpy())
print(UtilityFrame1_df.idxmax(axis= 1))
print(UtilityFrame2_df.idxmax(axis = 0))
"""
# To implement the no dictator game just make the whole action process creating into a function that has an
# if condition