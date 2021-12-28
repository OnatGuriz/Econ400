# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:07:32 2021

@author: cangu
"""
import itertools
import pandas as pd
from Functions import *
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

#https://blog.finxter.com/how-to-convert-a-string-list-to-an-integer-list-in-python/
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
    exit(1)

NECompute()
