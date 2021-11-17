Econ400
This program takes the talents of 2 agents ar_1 ar_2 as_1 as_2 then takes their respective budget constraints M_1 , M_2 and their possible action sets 

movesetSaving1 : all possible saving actions by agent 1 
movesetSaving2 : all possible saving actions by agent 2
movesetRecog1 : all possible recognition actions by agent 1
movesetrecog2 : all possible recognition actions by agent 2

this is for dictator game without budget transfers. If budget transfers are allowed we derive the action spaces from one set per player

From these the program creates 2 dataframes ActionFrame_df and UtilityFrame_df. 

ActionFrame_df : holds all possible action 4-tuples that are in the moveset lists.
UtilityFrame_df : holds all the possible payoffs that result from the actions in ActionFrame_df

Format of these dataframes are as follows:

Top: (e^1_s , e^1_r)
Left: (e^2_s , e^2_r) 
Payoffs: (EU_1,EU_2)

These dataframes are not shown in the Nash Equilibrium calculations. Format of the Nash Equilibrium is given in the output.

As a limitation if some action a is feasible in the dictator game with no budget transfers then M_i - a must also be in the action space. For example if an agent can choose to produce 0 or 250 when budget set is 400. Then the possible recognition values are 150 and 400. 

So not all transfer games are covered as of right now. 
