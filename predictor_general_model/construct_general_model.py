import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st

import sys
import math

# for measuring the efficiency/variability of the model
from sklearn.metrics import mean_absolute_error

# importing XGBoost API
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor

# importing joblib to save model as package
import joblib

# importing pathlib to handle paths to csv dataset
from pathlib import Path 

def obtain_X_y():
    file_path = Path(__file__).parent.parent.joinpath('Dataset', "processed-data-i1.csv")
    base_data_i1 = pd.read_csv(file_path)

    # declaring the independent paramaters
    x_features = ['Over','Inn_Score_atm','Inn_Wicks_atm','R_Rate_atm','Ptnr_Avg_atm','L3_Wicks','L3_Runs']
    X = base_data_i1[x_features]

    # target variable 
    y = base_data_i1.Runs_to_be_Scored

    return X,y

X,y = obtain_X_y()

# modelling the data
# model = XGBRegressor(n_estimators = 400, learning_rate=0.05)
model = RandomForestRegressor(n_estimators=100)
model.fit(X,y)

# saving the created model into a package file
joblib.dump(model, "gen_1st_inn_model.pkl") 

