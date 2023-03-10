import streamlit as st
import pandas as pd
import predictor_pro_model.build_and_run as build_and_run

st.markdown("# T20 Score Predictor")
st.sidebar.markdown("# T20 Score Predictor")
st.sidebar.markdown("## Pro Version")
st.sidebar.markdown("### For Local Execution Only")
st.sidebar.markdown("Selects appropriate data from the overall dataset based on number of overs remaining and wickets lost.")
st.sidebar.markdown("Trains a new ML model based on input data given.")
st.sidebar.markdown("Computationally expensive and advised to run a local copy of this application for execution.")

st.write("## Pro Version - For Local Execution Only")

col1,col2 = st.columns(2)
input_over = col1.number_input("Enter no of Overs played: ",min_value=5, max_value=19, step=1)
input_runs = col1.number_input("Enter runs scored in innings currently : ", min_value=0, step=1)
input_wick = col1.number_input("Enter number of Wickets Lost : ", min_value=0, max_value=9, step=1)
input_L3Sc = col2.number_input("Enter the Innings Total at the end of over no. " + str(input_over - 3) + " : ", min_value=0, max_value=int(input_runs), step=1)
input_L3Ws = col2.number_input("Enter number of wickets lost after over no. " + str(input_over-3) + " : ", min_value=0, max_value=int(input_wick), step=1)

input_RunR = round((input_runs/input_over),2)
st.markdown("**Current Run Rate : " + str(input_RunR) + "**")
input_L3Rs = input_runs - input_L3Sc
st.markdown("**Last 3 overs : " + str(input_L3Rs) + "/" + str(input_L3Ws) + "**")
input_PAvg = round((input_runs/(input_wick + 1)),2)

input_data = pd.DataFrame( {'Over' : [input_over] , 'Inn_Score_atm' : [input_runs] , 'Inn_Wicks_atm': [input_wick],
                            'R_Rate_atm': [input_RunR] ,  'Ptnr_Avg_atm': [input_PAvg] , 'L3_Wicks': [input_L3Ws],
                            'L3_Runs': [input_L3Rs] })

(min_score,max_score,pred_score,err,proj_RunR) = build_and_run.obtain_data_t20_i1(input_data)

if st.button("Predict"):
    build_and_run.display_outputs_i1(min_score,max_score,pred_score,err,proj_RunR)