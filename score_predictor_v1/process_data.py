import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import sys
import math

from pathlib import Path

file_path = Path(__file__).parent.parent.joinpath("Dataset","ball-by-ball-data.csv")
file = pd.read_csv(file_path)
file = file.dropna()

# Adding a column to record a loss of a wicket
file['dismissal_kind'] = file['dismissal_kind'].replace(' ',1)

dismissals =[]
for i in file.index: 
    if file.loc[i,'dismissal_kind'] == 1:
        dismissals.append(0)
    else:
        dismissals.append(1)

file['Wicket_Lost'] = dismissals

features = ['Match_id','Over','delivery','total_runs','Wicket_Lost']
file_inn1 = file[features].loc[file.Inning==1]
file_inn1['Inn_Score_atm'] = file_inn1.groupby('Match_id').total_runs.cumsum()
file_inn1['Inn_Wicks_atm'] = file_inn1.groupby('Match_id').Wicket_Lost.cumsum()

m1_id = file_inn1.groupby(['Match_id']).Inn_Score_atm.idxmax()
features1 = ['Match_id','Inn_Score_atm','Inn_Wicks_atm','Over']
match_1 = file_inn1.loc[m1_id,features1]
match_1 = match_1.rename(columns={'Inn_Score_atm': 'Final_Inning_Score'})
match_1 = match_1.rename(columns={'Inn_Wicks_atm': 'Final_Wickets_Lost'})
match_1 = match_1.rename(columns={'Over': 'Max_over_played'})

# to avoid selecting matches affected by rain and couldn't complete an ideal 20 overs
# let's take all the matches which managed to bat until a minumum of 16 overs or lost more than 8 wickets

# matches omitted from the model due to far from incomplete innings
# match.loc[((match.Max_over_played < 16)) & (match.Final_Wickets_Lost <= 8)]

match_1 = match_1.loc[((match_1.Max_over_played >= 16) & (match_1.Final_Wickets_Lost != 10)) |
                      (match_1.Final_Wickets_Lost > 8)]

# obtaining details about each over in the 1st innings as file_over1 database

a_id = file_inn1.groupby(['Match_id','Over']).delivery.idxmax()
features2 = ['Match_id','Over','Inn_Score_atm','Inn_Wicks_atm']
file_over1 = file_inn1.loc[a_id,features2]

# Run Rate at the end of each over of the 1st innings
file_over1['R_Rate_atm'] = round((file_over1.Inn_Score_atm / file_over1.Over),2)

# Average Patnership Score (Total Runs Scored/(No of Wickets + 1)) at the end of each over of 1st innings
file_over1['Ptnr_Avg_atm'] = round((file_over1.Inn_Score_atm / (file_over1.Inn_Wicks_atm+1)),2)

# Average Strike Rate of Wickets falling or No of balls on average a partnership stayed 
# (Total no of balls played / (No of wickets +1))
file_over1['Ptnr_Balls_atm'] = round(((file_over1.Over*6) / (file_over1.Inn_Wicks_atm+1)),2)

# Runs and Wickets Lost in the last 3 recent overs of the innings
file_over1['L3_Runs'] = file_over1.Inn_Score_atm - file_over1.Inn_Score_atm.shift(3)     
file_over1['L3_Wicks'] = file_over1.Inn_Wicks_atm - file_over1.Inn_Wicks_atm.shift(3)   

# The final database we use for our data prediction

base_data_i1 = match_1.set_index("Match_id").join(file_over1.set_index("Match_id"))
base_data_i1['Runs_to_be_Scored'] = base_data_i1['Final_Inning_Score'] - base_data_i1['Inn_Score_atm']
base_data_i1 = base_data_i1.loc[base_data_i1.Over > 3]

base_data_i1.to_csv("../T20-Cricket-Score-Predictor/Dataset/processed-data-i1.csv")
