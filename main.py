# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:07:32 2021

@author: cangu
"""
import itertools
import pandas as pd

# define the talents and budget

ar_1 = int(input("Recognition Talent of Agent 1: "))
ar_2 = int(input("Recognition Talent of Agent 2: "))
as_1 = int(input("Production Talent of Agent 1: "))
as_2 = int(input("Production Talent of Agent 2: "))

#defines wheter we have transfers or not
gametype = input("Transfer (T) or No Transfer (NT)")

#https://blog.finxter.com/how-to-convert-a-string-list-to-an-integer-list-in-python/
if(gametype == "NT"):
    movesetSaving1_input =  input("Enter all possible saving moves of agent 1 separated by space : ")
    movesetSaving2_input =  input("Enter all possible saving moves of agent 2 separated by space : ")
    movesetRecog1_input =  input("Enter all possible recognition moves of agent 1 separated by space : ")
    movesetRecog2_input =  input("Enter all possible recognition moves of agent 2 separated by space : ")

    movesetSaving1 = [int(value) for value in movesetSaving1_input.split()]
    movesetSaving2 = [int(value) for value in movesetSaving2_input.split()]
    movesetRecog1 = [int(value) for value in movesetRecog1_input.split()]
    movesetRecog2 = [int(value) for value in movesetRecog2_input.split()]

    M_1 = int(input("Agent 1 Budget: "))
    M_2 = int(input("Agent 2 Budget: "))

if (gametype == "T"):
    moveset_1_input = input("Enter all possible saving moves of agent 1 separated by space : ")
    moveset_1 = [int(value) for value in moveset_1_input.split()]
    moveset_2_input = input("Enter all possible saving moves of agent 2 separated by space : ")
    moveset_2 = [int(value) for value in moveset_2_input.split()]
    M_1 = int(input("Agent 1 Budget: "))
    M_2 = int(input("Agent 2 Budget: "))

#generate the action space for non-transfer games
#https://stackoverflow.com/questions/533905/get-the-cartesian-product-of-a-series-of-lists
def genActionSpace_NT(movesetSaving1, movesetSaving2, movesetRecog1, movesetRecog2):
    actionSpace1 = tuple(itertools.product(movesetSaving1, movesetRecog1))
    actionSpace2 = tuple(itertools.product(movesetSaving2, movesetRecog2))
    return actionSpace1, actionSpace2

#https://stackoverflow.com/questions/27891032/python-cartesian-product-and-conditions
def genActionSpace_T(moveset_1, moveset_2):
    movesetRecog1_T = []
    movesetRecog2_T = []
    movesetSaving1_T = moveset_1
    movesetSaving2_T = moveset_2
    for i in range(0, len(moveset_1)):
        movesetRecog1_T.append(M_1 - moveset_1[i])
    for i in range(0, len(moveset_2)):
        movesetRecog2_T.append(M_2 - moveset_2[i])
    actionSpace1 = list(itertools.product(movesetSaving1_T, movesetRecog1_T))
    actionSpace2 = list(itertools.product(movesetSaving2_T, movesetRecog2_T))
    actionSpace1 = list(filter(lambda x: x[0] + x[1] <= M_1, actionSpace1))
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
if (gametype == "NT"):
    Action_SpaceTotal = genActionSpace_NT(movesetSaving1, movesetSaving2, movesetRecog1, movesetRecog2)
elif (gametype == "T"):
    Action_SpaceTotal = genActionSpace_T(moveset_1, moveset_2)
else:
    print("choose a valid game")
    exit(1)

colnames = Action_SpaceTotal[0]
rownames = Action_SpaceTotal[1]

colnames_str = []
rownames_str = []

for i in range(0, len(colnames)):
    colnames_str.append(str(colnames[i]))

for j in range(0, len(rownames)):
    rownames_str.append(str(rownames[j]))

# row and columns for reference
# print("colnames: " + str(colnames))
# print("rownames: " + str(rownames))

# Here we set the row names and column names first
ActionFrame_df = pd.DataFrame(columns=colnames_str, index=rownames_str)
# then we assign their respective values
for i in range(0, len(rownames)):
    for j in range(0, len(colnames)):
        ActionFrame_df.iloc[j, i] = tuple((colnames[i] + rownames[j]))

"""" Format of the Dataframes
     Top : I^1_s , I^1_r
     Left: I^2_s , I^2_r
     Payoffs : (EU_1 , EU_2)
 """
# now we will compute all possible utilities on the action space dataframe to get utilities
# we will also create a reversed one for ease of computation
UtilityFrame1_df = ActionFrame_df.copy()
UtilityFrame2_df = ActionFrame_df.copy()
UtilityFrameTotal_df = ActionFrame_df.copy()

for i in range(0, len(rownames)):
    for j in range(0, len(colnames)):
        value = UtilityFrame1_df.iloc[i, j]
        UtilityFrame1_df.iloc[i, j] = utilFunc(value[0], value[1], value[2], value[3])[0]
        UtilityFrame2_df.iloc[i, j] = utilFunc(value[0], value[1], value[2], value[3])[1]
        UtilityFrameTotal_df.iloc[i, j] = utilFunc(value[0], value[1], value[2], value[3])
UtilityFrame1_df = UtilityFrame1_df.astype(float)
UtilityFrame2_df = UtilityFrame2_df.astype(float)


#finds the best response function with ties included
#sources:
#https://stackoverflow.com/questions/67230827/pandas-dataframe-select-column-by-boolean-values-in-matching-dataframe
#https://stackoverflow.com/questions/37362984/select-from-pandas-dataframe-using-boolean-series-array/37365260
#https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-which-column-matches-certain-value

def findBR(Payoff_1, Payoff_2):
    BR_1 = []
    BR_2 = []
    maxOfPl1 = UtilityFrame1_df.max(axis=1)
    maxOfPl2 = UtilityFrame2_df.max(axis=0)

    for i in range(0, len(colnames)):
        BR_1.append(UtilityFrame1_df.columns[UtilityFrame1_df.iloc[i,] == maxOfPl1[i]].to_list())
        for j in range(0, len(BR_1[i])):
            BR_1[i][j] = BR_1[i][j] + " , " + str(rownames[i])

    for i in range(0, len(rownames)):
        BR_2.append(UtilityFrame2_df.index[UtilityFrame2_df.iloc[:, i] == maxOfPl2[i]].to_list())
        for j in range(0, len(BR_2[i])):
            BR_2[i][j] = str(colnames[i]) + " , " + BR_2[i][j]

    return BR_1, BR_2


# format the best response functions in order to easily compute the NE
#https://stackoverflow.com/questions/3697432/how-to-find-list-intersection

def formatBR(l1):
    nl_1 = []
    for i in range(len(l1)):
        for j in range(len(l1[i])):
            if j > 0:
                nl_1.append(l1[i][j])
            else:
                nl_1.append(l1[i][0])
    return nl_1


finalBR_1 = formatBR(findBR(UtilityFrame1_df, UtilityFrame2_df)[0])
finalBR_2 = formatBR((findBR(UtilityFrame1_df, UtilityFrame2_df))[1])


NE = list(set(finalBR_1) & set(finalBR_2))
if NE != []:
    print("Nash Equilibrium/Equilibria is/are " + str(NE))
    print("Format is ['(e^s_1 , e^r_1 ),(e^s_2 , e^r_2)']")
else:
    print("There seems to be no pure strategy NE")
    print("If you are sure there is one notify Can Güriz")
