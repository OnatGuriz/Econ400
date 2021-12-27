# In this file we have all the required functions
import pandas as pd
import itertools
import config


# generate the action space for non-transfer games
# https://stackoverflow.com/questions/533905/get-the-cartesian-product-of-a-series-of-lists
def genActionSpace_NT(movesetSaving1, movesetSaving2, movesetRecog1, movesetRecog2):
    actionSpace1 = tuple(itertools.product(movesetSaving1, movesetRecog1))
    actionSpace2 = tuple(itertools.product(movesetSaving2, movesetRecog2))
    return actionSpace1, actionSpace2

# generate actionspace for transfer games
# https://stackoverflow.com/questions/27891032/python-cartesian-product-and-conditions
def genActionSpace_T(movesetS_1,movesetR_1,movesetS_2 ,movesetR_2):
    movesetRecog1_T = movesetR_1
    movesetRecog2_T = movesetR_2
    movesetSaving1_T = movesetS_1
    movesetSaving2_T = movesetS_2
    actionSpace1 = list(itertools.product(movesetSaving1_T, movesetRecog1_T))
    actionSpace2 = list(itertools.product(movesetSaving2_T, movesetRecog2_T))
    actionSpace1 = list(filter(lambda x: x[0] + x[1] <= config.M_1, actionSpace1))
    actionSpace2 = list(filter(lambda x: x[0] + x[1] <= config.M_2, actionSpace2))
    return actionSpace1, actionSpace2

# decide which game is played and create space accordingly
def generateAC (gametype, movesetSaving1, movesetSaving2, movesetRecog1, movesetRecog2, movesetS_1, movesetR_1,movesetS_2,movesetR_2):
    if (gametype == "NT"):
        config.Action_SpaceTotal = genActionSpace_NT(movesetSaving1, movesetSaving2, movesetRecog1, movesetRecog2)
    elif (gametype == "T"):
        config.Action_SpaceTotal = genActionSpace_T(movesetS_1,movesetR_1,movesetS_2,movesetR_2)
    else:
        print("choose a valid game")
        exit(1)

# makes all the moves as strings to put into the dataframes later
def namesStrGen(rowmanes,colnames):
    colnames_str = []
    rownames_str = []

    for i in range(0, len(config.colnames)):
        colnames_str.append(str(config.colnames[i]))

    for j in range(0, len(config.rownames)):
        rownames_str.append(str(config.rownames[j]))

    config.rownames_str = rownames_str
    config.colnames_str = colnames_str

# computing the output
def prodFunc(es_1, es_2):
    return (es_1 * config.as_1 + es_2 * config.as_2)


# computing recognition probabilities
def recogProb(er_1, er_2):
    if er_1 == 0 and er_2 == 0:
        return 0.5, 0.5
    else:
        p1_recog = (config.ar_1 * er_1) / (config.ar_1 * er_1 + config.ar_2 * er_2)
        p2_recog = 1 - p1_recog
        return ((p1_recog, p2_recog))


# computing the estimated utilities with 2 decimals
def utilFunc(es_1, er_1, es_2, er_2):
    EU_1 = round((recogProb(er_1, er_2)[0] * prodFunc(es_1, es_2)) + (config.M_1 - es_1 - er_1), 2)
    EU_2 = round((recogProb(er_1, er_2)[1] * prodFunc(es_1, es_2)) + (config.M_2 - es_2 - er_2), 2)
    return EU_1, EU_2


# finds the best response function with ties included
# sources:
# https://stackoverflow.com/questions/67230827/pandas-dataframe-select-column-by-boolean-values-in-matching-dataframe
# https://stackoverflow.com/questions/37362984/select-from-pandas-dataframe-using-boolean-series-array/37365260
# https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-which-column-matches-certain-value
def findBR(Payoff_1, Payoff_2):
    BR_1 = []
    BR_2 = []
    maxOfPl1 = config.UtilityFrame1_df.max(axis=1)
    maxOfPl2 = config.UtilityFrame2_df.max(axis=0)

    for i in range(0, len(config.colnames)):
        BR_1.append(config.UtilityFrame1_df.columns[config.UtilityFrame1_df.iloc[i,] == maxOfPl1[i]].to_list())
        for j in range(0, len(BR_1[i])):
            BR_1[i][j] = BR_1[i][j] + " , " + str(config.rownames[i])

    for i in range(0, len(config.rownames)):
        BR_2.append(config.UtilityFrame2_df.index[config.UtilityFrame2_df.iloc[:, i] == maxOfPl2[i]].to_list())
        for j in range(0, len(BR_2[i])):
            BR_2[i][j] = str(config.colnames[i]) + " , " + BR_2[i][j]

    return BR_1, BR_2

# format the best response functions in order to easily compute the NE
# https://stackoverflow.com/questions/3697432/how-to-find-list-intersection
def formatBR(l1):
    nl_1 = []
    for i in range(len(l1)):
        for j in range(len(l1[i])):
            if j > 0:
                nl_1.append(l1[i][j])
            else:
                nl_1.append(l1[i][0])
    return nl_1

# compute the Nash Equilibrium using the values in config
def NECompute ():
    generateAC(config.gametype, config.movesetSaving1, config.movesetSaving2, config.movesetRecog1,
               config.movesetRecog2, config.movesetS_1, config.movesetR_1, config.movesetS_2, config.movesetR_2)

    config.colnames = config.Action_SpaceTotal[0]
    config.rownames = config.Action_SpaceTotal[1]

    namesStrGen(config.rownames, config.colnames)

    # Here we set the row names and column names first
    config.ActionFrame_df = pd.DataFrame(columns=config.colnames_str, index=config.rownames_str)
    # then we assign their respective values
    for i in range(0, len(config.rownames)):
        for j in range(0, len(config.colnames)):
            config.ActionFrame_df.iloc[j, i] = tuple((config.colnames[i] + config.rownames[j]))

    config.UtilityFrame1_df = config.ActionFrame_df.copy()
    config.UtilityFrame2_df = config.ActionFrame_df.copy()
    config.UtilityFrameTotal_df = config.ActionFrame_df.copy()
    for i in range(0, len(config.rownames)):
        for j in range(0, len(config.colnames)):
            value = config.UtilityFrame1_df.iloc[i, j]
            config.UtilityFrame1_df.iloc[i, j] = utilFunc(value[0], value[1], value[2], value[3])[0]
            config.UtilityFrame2_df.iloc[i, j] = utilFunc(value[0], value[1], value[2], value[3])[1]
            config.UtilityFrameTotal_df.iloc[i, j] = utilFunc(value[0], value[1], value[2], value[3])
    config.UtilityFrame1_df = config.UtilityFrame1_df.astype(float)
    config.UtilityFrame2_df = config.UtilityFrame2_df.astype(float)

    finalBR_1 = formatBR(findBR(config.UtilityFrame1_df, config.UtilityFrame2_df)[0])
    finalBR_2 = formatBR((findBR(config.UtilityFrame1_df, config.UtilityFrame2_df))[1])
    config.NE = list(set(finalBR_1) & set(finalBR_2))
    if config.NE != []:
        print("Nash Equilibrium/Equilibria is/are " + str(config.NE))
        print("Format is ['(e^s_1 , e^r_1 ),(e^s_2 , e^r_2)']")
    else:
        print("There seems to be no pure strategy NE")



