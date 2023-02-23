import streamlit as st
import pandas as pd
import joblib
import predictor_pro_model.build_and_run as build_and_run
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder

st.markdown("# Timeline of Final Predicted Score")
st.sidebar.markdown("# Timeline of Final Predicted Score")
st.sidebar.markdown("## Pro Version")
st.sidebar.markdown("### For Local Execution Only")
st.sidebar.markdown("**Use to visualize the variation in the Score Prediction at each stage of the innings.**")
st.sidebar.markdown("Implemented using the specialized data selection machine learning model for the predictions.")
st.sidebar.markdown("Computationally expensive and advised to run a local copy of this application for execution.")
st.sidebar.markdown("May take a few seconds to run.")
st.sidebar.markdown("You can start entering data at any point of the game.")
st.sidebar.markdown("Note you need at least 4 entries of data to generate the first prediction.")

st.write("## Pro Version - For Local Execution Only")
st.markdown("#### Enter the Input Runs Scored and Wickets Lost at the end of the overs given below as the match goes along")
st.markdown("#### Click on the _Submit_ button below to generate the predictor chart for data enetered.")
st.markdown("###### You can start entering data at any point of the game.")
st.markdown("###### Note you need at least 4 entries of data to generate the first prediction.")

df_template = pd.DataFrame(
    '',
    index=range(18),
    columns=['Over','Current Score','Wickets Lost']
)

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
    if (response.data.loc[i,'Current Score'] == "") | (response.data.loc[i,'Wickets Lost'] == ""):
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

    response.data.loc[i,'Runs in the Over'] = input_runs - int(response.data.loc[i-1,'Current Score'])
    response.data.loc[i,'Wickets in the Over'] = input_wick - int(response.data.loc[i-1,'Wickets Lost'])

    (min_score,max_score,pred_score,err,proj_RunR) = build_and_run.obtain_data_t20_i1(input_data)

    response.data.loc[i,'Current RunRate'] = round(input_runs/input_over,2)
    response.data.loc[i,'Prediction'] = pred_score
    response.data.loc[i,'+/-'] = err
    response.data.loc[i,'Min Prediction'] = min_score
    response.data.loc[i,'Max Prediction'] = max_score
    response.data.loc[i,'Projected RunRate'] = round(proj_RunR,2)

if button:

    fig = make_subplots(specs=[[{"secondary_y" : True}]])
    fig.add_trace(
        go.Bar(x=response.data.loc[3:,"Over"], y=response.data.loc[3:,"Runs in the Over"], name = "Runs in Over"
               ,marker=dict(color="#4ECCED"),opacity=0.5)
        , secondary_y=True   
    )
    fig.add_trace(
        go.Bar(x=response.data.loc[3:,"Over"], y=response.data.loc[3:,"Wickets in the Over"], name = "Wickets Fallen in Over"
               ,marker=dict(color="#ff9835"),opacity=0.5)
        , secondary_y=True   
    )
    fig.add_trace(
        go.Line(x=response.data.loc[3:,"Over"], y=response.data.loc[3:,"Prediction"], name='Prediction',line=dict(color="#FFE400"))
    )
    fig.add_trace(
        go.Line(x=response.data.loc[3:,"Over"], y=response.data.loc[3:,"Min Prediction"], name='Min Prediction',line=dict(color="#00FF00"))
    )
    fig.add_trace(
        go.Line(x=response.data.loc[3:,"Over"], y=response.data.loc[3:,"Max Prediction"], name='Max Prediction',line=dict(color="#FF00CA"))
    )

    fig.update_layout(
        title_text = "Score Prediction Variation Throughout the Match"
    )
    fig.update_xaxes(title_text="Over")
    fig.update_yaxes(title_text="Final Score Predictions",secondary_y=False)
    fig.update_yaxes(title_text="Runs Scored or Wickets Lost per Over", secondary_y=True)
    fig.update_layout(yaxis2_range=[0,40])
    fig.update_yaxes(secondary_y=True, showgrid=False)
    st.plotly_chart(fig)

    st.markdown("**Score Predictions Tabulated**")
    cols_to_display = ['Over','Prediction','+/-','Current RunRate','Projected RunRate']
    st.write(response.data.loc[3:,cols_to_display])