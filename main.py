# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:07:32 2021

@author: cangu
"""
from Functions import *
import matplotlib.pyplot as plt
import config

inputOrNo = input("Do you want to input the values Y/N?")

# define the talents and budget
if(inputOrNo == "Y"):
    config.ar_1 = int(input("Recognition Talent of Agent 1: "))
    config.ar_2 = int(input("Recognition Talent of Agent 2: "))
    config.as_1 = int(input("Production Talent of Agent 1: "))
    config.as_2 = int(input("Production Talent of Agent 2: "))


#defines wheter we have transfers or not
if(inputOrNo == "Y"):
    config.gametype = input("Transfer (T) or No Transfer (NT)")

#Do we want to compute NE with an input or not
if (inputOrNo == "Y"):
    if(config.gametype == "NT"):
        movesetSaving1_input =  input("Enter all possible saving moves of agent 1 separated by space : ")
        movesetSaving2_input =  input("Enter all possible saving moves of agent 2 separated by space : ")
        movesetRecog1_input =  input("Enter all possible recognition moves of agent 1 separated by space : ")
        movesetRecog2_input =  input("Enter all possible recognition moves of agent 2 separated by space : ")

        config.movesetSaving1 = [int(value) for value in movesetSaving1_input.split()]
        config.movesetSaving2 = [int(value) for value in movesetSaving2_input.split()]
        config.movesetRecog1 = [int(value) for value in movesetRecog1_input.split()]
        config.movesetRecog2 = [int(value) for value in movesetRecog2_input.split()]
        config.M_1 = int(input("Agent 1 Budget: "))
        config.M_2 = int(input("Agent 2 Budget: "))

    if (config.gametype == "T"):
        movesetS_1_input = input("Enter all possible saving moves of agent 1 separated by space : ")
        config.movesetS_1 = [int(value) for value in movesetS_1_input.split()]
        movesetS_2_input = input("Enter all possible saving moves of agent 2 separated by space : ")
        config.movesetS_2 = [int(value) for value in movesetS_2_input.split()]
        movesetR_1_input = input("Enter all possible recognition moves of agent 1 separated by space : ")
        config.movesetR_1 = [int(value) for value in movesetR_1_input.split()]
        movesetR_2_input = input("Enter all possible recognition moves of agent 1 separated by space : ")
        config.movesetR_2 = [int(value) for value in movesetR_2_input.split()]
        config.M_1 = int(input("Agent 1 Budget: "))
        config.M_2 = int(input("Agent 2 Budget: "))

if (inputOrNo == "N"):
    config.gametype = "T"
    config.movesetSaving1 = [0, 100 , 200 , 300 , 400]
    config.movesetSaving2 = [0, 100 , 200 , 300 , 400]
    config.movesetRecog1 = [0, 100 , 200 , 300 , 400]
    config.movesetRecog2 = [0, 100 , 200 , 300 , 400]

    config.movesetS_1 = [0, 100 , 200 , 300 , 400]
    config.movesetS_2 = [0, 100 , 200 , 300 , 400]
    config.movesetR_1 = [0, 100 , 200 , 300 , 400]
    config.movesetR_2 = [0, 100 , 200 , 300 , 400]

    config.M_1 = 400
    config.M_2 = 400

    config.ar_1 = 2
    config.ar_2 = 1
    config.as_1 = 9
    config.as_2 = 3

#seperates the Nash Eqm into players moves in order to graph
def sortresult(input):
    pl_1_r = []
    pl_1_s = []
    pl_2_r = []
    pl_2_s = []
    for i in range (0, len(input)):
        if i % 2 == 0:
            pl_1_s.append(input[i][0])
            pl_1_r.append(input[i][1])
        if i % 2 == 1:
            pl_2_s.append(input[i][0])
            pl_2_r.append(input[i][1])
    return pl_1_s , pl_1_r , pl_2_s, pl_2_r

config.SavingTalents = [1, 2, 3 ,4 ,5 ,6, 7, 8 , 9 ,10]
config.RecogTalents = [1, 2, 3, 4, 5, 6, 7,8 , 9 ,10]

print(NECompute())
print(sortresult(getValueNE()))

def Grapher(variable_name):
    resultpl_1_s = []
    resultpl_1_r = []
    resultpl_2_s = []
    resultpl_2_r = []
    resultNE = []
    if(variable_name == "Saving"):
        var = config.SavingTalents
    if(variable_name == "Recognition"):
        var = config.RecogTalents
    for value in var:
        if(variable_name == "Saving"):
            config.as_1 = value
        elif(variable_name == "Recognition"):
            config.ar_1 = value
        else:
            exit(2)
        resultNE = sortresult(getValueNE())
        if (resultNE != ([],[],[],[])):
            resultpl_1_s.append(resultNE[0])
            resultpl_1_r.append(resultNE[1])
            resultpl_2_s.append(resultNE[2])
            resultpl_2_r.append(resultNE[3])
        if(resultNE == ([],[],[],[])):
            resultpl_1_s.append("NaN")
            resultpl_1_r.append("NaN")
            resultpl_2_s.append("NaN")
            resultpl_2_r.append("NaN")
    resdict_1_s = {}
    resdict_1_r = {}
    resdict_2_s = {}
    resdict_2_r = {}

    for i in range(len(config.SavingTalents)):
        resdict_1_s[config.SavingTalents[i]] = resultpl_1_s[i]
        resdict_1_r[config.SavingTalents[i]] = resultpl_1_r[i]
        resdict_2_s[config.SavingTalents[i]] = resultpl_2_s[i]
        resdict_2_r[config.SavingTalents[i]] = resultpl_2_r[i]

    return resdict_1_s,resdict_1_r , resdict_2_s, resdict_2_r



print(Grapher("Saving")[0])

#ToDo graph the dictionaries with respect to the keys