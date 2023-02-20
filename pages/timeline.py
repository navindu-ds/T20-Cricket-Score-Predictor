import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

st.markdown("# Timeline of Final Predicted Score")
st.sidebar.markdown("# Timeline of Final Predicted Score")
st.sidebar.markdown("Check how the Score Prediction varies at each stage of the match")

from st_aggrid import AgGrid, GridOptionsBuilder

df_template = pd.DataFrame(
    '',
    index=range(18),
    columns=['Over','Current Score','Wickets Lost']
)

df_template['Prediction'] = 0

for x in df_template.index.values:
    df_template.loc[x,'Over'] = x + 2

gb = GridOptionsBuilder.from_dataframe(df_template)
gb.configure_column("Over", editable=False)
gb.configure_columns(["Current Score","Wickets Lost"], editable = True)
gb.configure_default_column(min_column_width=7)
gridOptions = gb.build()

with st.form('example form') as f:
    st.header('Input Runs Scored and Wickets Lost at each over of the match')
    response = AgGrid(df_template, gridOptions=gridOptions, columns_auto_size_mode=True, fit_columns_on_grid_load=False)
    button = st.form_submit_button()

model = joblib.load('gen_1st_inn_model.pkl')

for i in range(3,18):
    if (response.data.loc[i,'Over'] == "") | (response.data.loc[i,'Current Score'] == "") | (response.data.loc[i,'Wickets Lost'] == ""):
        continue
    if (response.data.loc[i-3,'Current Score'] == "") | (response.data.loc[i-3,'Wickets Lost'] == ""):
        continue
    input_over = int(response.data.loc[i,'Over'])
    input_runs = int(response.data.loc[i,'Current Score'])
    input_wick = int(response.data.loc[i,'Wickets Lost'])
    input_RunR = round((input_runs/input_over),2)
    input_PAvg = round((input_runs/(input_wick + 1)),2)
    input_L3Ws = input_wick - int(response.data.loc[i-3,'Wickets Lost'])
    input_L3Rs = input_runs - int(response.data.loc[i-3,'Current Score'])

    input_data = pd.DataFrame( {'Over' : [input_over] , 'Inn_Score_atm' : [input_runs] , 'Inn_Wicks_atm': [input_wick],
                            'R_Rate_atm': [input_RunR] ,  'Ptnr_Avg_atm': [input_PAvg] , 'L3_Wicks': [input_L3Ws],
                            'L3_Runs': [input_L3Rs] })

    response.data.loc[i,'Prediction'] = input_runs + int(model.predict(input_data))

if button:
    st.write(response.data.loc[3:])

fig = px.line(x=response.data.loc[3:,"Over"], y=response.data.loc[3:,"Prediction"], title='Variation in Prediction across the match')
fig.show()
