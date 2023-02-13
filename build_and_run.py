import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st

import sys
import math

# for measuring the efficiency/variability of the model
from sklearn.metrics import mean_absolute_error

# importing XGBoost API
from xgboost import XGBRegressor

# importing joblib to save model as package
import joblib

file_path = "../T20-Cricket-Score-Predictor/Dataset/processed-data-i1.csv"
base_data_i1 = pd.read_csv(file_path)

global input_data

def obtain_data_t20_i1(input_data):

    input_over = input_data.iloc[0,0]
    input_wick = input_data.iloc[0,2]
    input_L3Ws = input_data.iloc[0,5]
    input_L3Rs = input_data.iloc[0,6]

    global overs_req
    global wicks_req
    global data_base
    
    # our base dataframe is base_data_i1
    
    # required rows of data to model fromwhich are played within +/- 3 overs of the input_over
    overs_req = (
                 (base_data_i1.Over == (input_over-3)) | (base_data_i1.Over == (input_over-2)) | 
                 (base_data_i1.Over == (input_over-1)) | (base_data_i1.Over == (input_over+0)) | 
                 (base_data_i1.Over == (input_over+1)) | (base_data_i1.Over == (input_over+2)) | 
                 (base_data_i1.Over == (input_over+3))
                )
    
    # required rows of data to model from which are played having lost +/- 1 wicket of the input_wick
    wicks_req = ((base_data_i1.Inn_Wicks_atm == (input_wick-1)) | (base_data_i1.Inn_Wicks_atm == (input_wick)) |
                 (base_data_i1.Inn_Wicks_atm == (input_wick+1))
                )
    # required rows of data to model from which the same number of wickets have been lost in the preceeding 3 overs
    L3WLs_req = base_data_i1.L3_Wicks == input_L3Ws
    
    # required rows of data to model from which the similar run scoring in the preceeding 3 overs
    L3RSc_req = ((base_data_i1.L3_Runs == (input_L3Rs-3)) | (base_data_i1.L3_Runs == (input_L3Rs-2)) |
                 (base_data_i1.L3_Runs == (input_L3Rs-1)) | (base_data_i1.L3_Runs == (input_L3Rs-0)) |
                 (base_data_i1.L3_Runs == (input_L3Rs+1)) | (base_data_i1.L3_Runs == (input_L3Rs+2)) |
                 (base_data_i1.L3_Runs == (input_L3Rs+3))
                )
    
    # extracting required data from the either of the two criteria above
    data_base = base_data_i1.loc[ overs_req | wicks_req | L3WLs_req | L3RSc_req ] 
    
    # st.write('>> Calculating from ' + str(data_base.Over.count()) + ' similar instances.')
    
    #calling out the next function
    (min_score,max_score,pred_score,err,proj_RunR) = select_features_i1(data_base, input_data)
    
    return (min_score,max_score,pred_score,err,proj_RunR)

def select_features_i1(data_base, input_data):
    # independent and input variables features
    x_features = ['Over','Inn_Score_atm','Inn_Wicks_atm','R_Rate_atm','Ptnr_Avg_atm','L3_Wicks','L3_Runs']
    X = data_base[x_features]
    
    # target variable 
    y = data_base.Runs_to_be_Scored
    
    # calling out the next function
    XGB_model = data_modelling(X,y)
    
    # saving the created model into a package file
    joblib.dump(XGB_model, '1st_innings_model.pkl') 
    
    #calling out the next function
    (expected_runs, err) = obtain_values(XGB_model,X,y, input_data)
    
    #calling out next function
    (min_score,max_score,pred_score,err,proj_RunR)= design_output_i1(expected_runs,err,input_data.iloc[0,1],input_data.iloc[0,0])

    return (min_score,max_score,pred_score,err,proj_RunR)

def data_modelling(X,y):
    # programming the model
    XGB_model = XGBRegressor(n_estimators = 400, learning_rate=0.05)
    XGB_model.fit(X,y)
    return XGB_model

def obtain_values(XGB_model,X,y, input_data):
    input_runs = input_data.iloc[0,1]

    # obatining the predictions
    pred_y = XGB_model.predict(X)
    
    # error measured by mean_absolute_error according to predicted and actual target values
    err = int(mean_absolute_error(y, pred_y))
    
    # adjusting error depending on over                                                   # this was obtained by trial and
    err_adj_1 = math.log(-27+50,(math.e**math.sqrt(12)))                                     # error
    
    # adjusting error depending on prediction of score
    expected_runs = int(XGB_model.predict(input_data))
    expected_percent = round( (abs(expected_runs) / (input_runs+expected_runs) ),2)*100.
    err_adj_2 = math.log(expected_percent,(math.e**math.sqrt(16)))
    
    # error value
    err = err * (err_adj_1 * err_adj_2) ** (1/2)
    err = int(err)
    return expected_runs,err

def design_output_i1(expected_runs,err,input_runs,input_over):
    
    # developing outputs
    pred_score = input_runs + expected_runs
    max_score  = int(pred_score + err)
    min_score  = int(pred_score - err)
    proj_RunR  = round((expected_runs/(20-input_over)),2)
    
    if min_score < input_runs:
        min_score = input_runs + 5
    else:
        pass
    return min_score,max_score,pred_score,err,proj_RunR


def display_outputs_i1(min_score, max_score, pred_score, err, proj_RunR):
    # printing out the output predictions
    st.write('### PREDICTION : ' + str(pred_score))
    st.write('##### VARIANCE IN PREDICTION : +/-' + str(int(err)))
    st.write('##### RANGE OF INNINGS TOTAL : ' + str(min_score) + ' to ' + str(max_score))
    st.write('##### PROJECTED RUN RATE FOR REMAINDER OF THE INNINGS : ' + str(proj_RunR))