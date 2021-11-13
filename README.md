Econ400
This program takes the talents of 2 agents ar_1 ar_2 as_1 as_2 then takes their respective budget constraints M_1 , M_2 and their possible action sets 

movesetSaving1 : all possible saving actions by agent 1 
movesetSaving2 : all possible saving actions by agent 2
movesetRecog1 : all possible recognition actions by agent 1
movesetrecog2 : all possible recognition actions by agent 2

this is for dictator game without budget transfers. If budget transfers are allowed then one set per agent is sufficient to derive an action space.

From these the program creates 2 dataframes ActionFrame_df and UtilityFrame_df. 

ActionFrame_df : holds all possible action 4-tuples that are in the moveset lists.
UtilityFrame_df : holds all the possible payoffs that result from the actions in ActionFrame_df

Format of these dataframes are as follows:

Top: (e^1_s , e^1_r)
Left: (e^2_s , e^2_r) 
Payoffs: (EU_1,EU_2)

The program also checks if any element of the moveset violates the budget or non-negativity constraints if no constraints are violated the following output will occur

no problem in agent 1 saving choices
no problem in agent 1 recognition choices
no problem in agent 2 saving choices
no problem in agent 2 recognition choices

if any of these are missing from the console log then there is a problem with the action sets that are given (currently not done)

