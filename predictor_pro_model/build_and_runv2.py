import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st
import math

# for measuring the efficiency/variability of the model
from sklearn.metrics import mean_absolute_error

# importing XGBoost API
from xgboost import XGBRegressor

# importing joblib to save model as package
import joblib

# importing pathlib to handle paths to csv dataset
from pathlib import Path 

file_path = Path(__file__).parent.parent.joinpath('Dataset', "processed-data-i1.csv")
base_data_i1 = pd.read_csv(file_path)

def obtain_data_t20_i1(input_data, dataset):
    input_over = input_data.iloc[0,0]
    input_wick = input_data.iloc[0,2]
    input_L3Ws = input_data.iloc[0,5]
    input_L3Rs = input_data.iloc[0,6]

    # our base dataframe is dataset
    
    # required rows of data to model fromwhich are played within +/- 3 overs of the input_over
    overs_req = ((dataset.Over >= input_over-3) & (dataset.Over <= input_over+3))

    # required rows of data to model from which are played having lost +/- 1 wicket of the input_wick
    wicks_req = ((dataset.Inn_Wicks_atm >= input_wick-1) & (dataset.Inn_Wicks_atm <= input_wick+1))

    # required rows of data to model from which the same number of wickets have been lost in the preceeding 3 overs
    L3WLs_req = base_data_i1.L3_Wicks == input_L3Ws

    # required rows of data to model from which the similar run scoring in the preceeding 3 overs
    L3RSc_req = ((dataset.L3_Runs >= input_L3Rs-3) & (dataset.L3_Runs <= input_L3Rs+3))

    # extracting required data from the either of the two criteria above
    data_base = base_data_i1[overs_req & (wicks_req | L3WLs_req | L3RSc_req)]

    print(f"Size of Data Base {len(data_base)} out of {len(dataset)}")

    return data_base

def select_features_i1(data_base):
    # independent and input variables features
    x_features = ['Over','Inn_Score_atm','Inn_Wicks_atm','R_Rate_atm','Ptnr_Avg_atm','L3_Wicks','L3_Runs']
    X = data_base[x_features]

    # target variable 
    y = data_base.Runs_to_be_Scored

    return X, y

def ReLU(x):
    return (np.maximum(0, x))

def create_train_modelv1(X, y):
    # programming the model
    XGB_model = XGBRegressor(n_estimators = 400, learning_rate=0.05)
    XGB_model.fit(X, y)

    # saving the created model into a package file
    joblib.dump(XGB_model, '1st_innings_model.pkl') 
    
    return XGB_model

def create_train_modelv2(X, y, train_percent):
    train_len = int(len(X)*train_percent)
    train_X, test_X = X[:train_len], X[train_len:]
    train_y, test_y = y[:train_len], y[train_len:]
    
    # programming the model
    XGB_model = XGBRegressor(n_estimators = 400, learning_rate=0.05)
    XGB_model.fit(train_X,train_y)

    # saving the created model into a package file
    # joblib.dump(XGB_model, '1st_innings_model.pkl') 

    train_err = obtain_error(XGB_model, train_X, train_y)
    print(f"Train Error: {train_err}")

    test_err = obtain_error(XGB_model, test_X, test_y)
    print(f"Test Error: {test_err}")

    return XGB_model

def obtain_error(model, X, y):
    pred_y = ReLU(model.predict(X).round())
    err = round(mean_absolute_error(y, pred_y), 2)
    # print(pred_y)
    return err

def display_outputs_i1(min_score, max_score, pred_score, err, proj_RunR):
    # printing out the output predictions
    st.write('### PREDICTION : ' + str(pred_score))
    st.write('##### VARIANCE IN PREDICTION : +/-' + str(int(err)))
    st.write('##### RANGE OF INNINGS TOTAL : ' + str(min_score) + ' to ' + str(max_score))
    st.write('##### PROJECTED RUN RATE FOR REMAINDER OF THE INNINGS : ' + str(proj_RunR))

def predict_t20_i1(input):
    input_runs = input.iloc[0,1]
    input_over = input.iloc[0,0]

    selected_data_base = obtain_data_t20_i1(input, base_data_i1)

    sel_X, sel_y = select_features_i1(selected_data_base)

    model = create_train_modelv1(sel_X, sel_y)

    expected_runs = int(model.predict(input))

    err = obtain_error(model, sel_X, sel_y)

    pred_score = input_runs + expected_runs
    max_score = int(pred_score + err)
    min_score = int(pred_score - err)
    min_score = max(input_runs,min_score)
    proj_RunR = round((expected_runs/(20 - input_over)), 2)

    display_outputs_i1(min_score, max_score, pred_score, err, proj_RunR)

# input_data = pd.DataFrame( {'Over' : [5] , 'Inn_Score_atm' : [36] , 'Inn_Wicks_atm': [2],
#                                 'R_Rate_atm': [7.20] ,  'Ptnr_Avg_atm': [12.00] , 'L3_Wicks': [1],
#                                 'L3_Runs': [20] })

# input_data = pd.DataFrame( {'Over' : [11] , 'Inn_Score_atm' : [95] , 'Inn_Wicks_atm': [3],
#                                 'R_Rate_atm': [8.64] ,  'Ptnr_Avg_atm': [23.75] , 'L3_Wicks': [1],
#                                 'L3_Runs': [23] })

# input_data = pd.DataFrame( {'Over' : [15] , 'Inn_Score_atm' : [117] , 'Inn_Wicks_atm': [6],
#                                 'R_Rate_atm': [7.80] ,  'Ptnr_Avg_atm': [16.71] , 'L3_Wicks': [1],
#                                 'L3_Runs': [117-85] })

# input_data = pd.DataFrame( {'Over' : [18] , 'Inn_Score_atm' : [147] , 'Inn_Wicks_atm': [6],
#                                 'R_Rate_atm': [8.16] ,  'Ptnr_Avg_atm': [21] , 'L3_Wicks': [0],
#                                 'L3_Runs': [30] })

# input_data = pd.DataFrame( {'Over' : [10] , 'Inn_Score_atm' : [39] , 'Inn_Wicks_atm': [8],
#                                 'R_Rate_atm': [3.9] ,  'Ptnr_Avg_atm': [4.33] , 'L3_Wicks': [3],
#                                 'L3_Runs': [14] })

# predict_t20_i1(input_data)