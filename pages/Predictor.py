import streamlit as st
import pandas as pd
import joblib

st.markdown("# T20 Score Predictor")
st.sidebar.markdown("# T20 Score Predictor")
st.sidebar.markdown("Use for one-off predictions")
st.sidebar.markdown("Uses a single pre-processed machine learning model to be applied for all scenarios of the game.")
st.sidebar.markdown("Easy to deploy online and computationally cost efficient.")
st.sidebar.markdown("Model for computing variance in final prediction is not yet available in this version.")

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

model = joblib.load('gen_1st_inn_model.pkl')
expected_runs = int(model.predict(input_data))
projRunR = round((expected_runs/(20-input_over)),2)

if st.button("Predict"):
    st.write("### PREDICTION " + str(expected_runs + input_runs))
    st.write("##### PROJECTED RUN RATE FOR REMAINDER OF THE INNINGS : " + str(projRunR))