import streamlit as st
import pandas as pd
import joblib
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder

st.markdown("# Timeline of Final Predicted Score")
st.sidebar.markdown("# Timeline of Final Predicted Score")
st.sidebar.markdown("**Use to visualize the variation in the Score Prediction at each stage of the innings.**")
st.sidebar.markdown("Implemented using the web version machine learning model for the predictions.")
st.sidebar.markdown("You can start entering data at any point of the game.")
st.sidebar.markdown("Note you need at least 4 entries of data to generate the first prediction.")

if (st.session_state):
    # Show the page content
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

    st.markdown("#### Enter the Input Runs Scored and Wickets Lost at the end of the overs given below as the match goes along")
    st.markdown("#### Click on the _Submit_ button below to generate the predictor chart for data enetered.")
    st.markdown("###### You can start entering data at any point of the game.")
    st.markdown("###### Note you need at least 4 entries of data to generate the first prediction.")
    with st.form('example form') as f:
        st.header('Enter Over-by-Over data')
        response = AgGrid(df_template, gridOptions=gridOptions, columns_auto_size_mode=True, fit_columns_on_grid_load=False)
        button = st.form_submit_button("Submit")

        if button:
            pass 

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

        prediction =  input_runs + int(model.predict(input_data))
        response.data.loc[i,'Current RunRate'] = round(input_runs/input_over,2)
        response.data.loc[i,'Runs in the Over'] = input_runs - int(response.data.loc[i-1,'Current Score'])
        response.data.loc[i,'Wickets in the Over'] = input_wick - int(response.data.loc[i-1,'Wickets Lost'])
        response.data.loc[i,'Prediction'] = prediction
        response.data.loc[i,'Projected RunRate'] = round((prediction-input_runs)/(20-input_over))

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
            go.Line(x=response.data.loc[3:,"Over"], y=response.data.loc[3:,"Prediction"], name='Prediction',line=dict(color="#00ff00"))
        )
        fig.update_layout(
            title_text = "Score Prediction Variation Throughout the Match"
        )
        fig.update_xaxes(title_text="Over")
        fig.update_yaxes(title_text="Final Score Prediction",secondary_y=False)
        fig.update_yaxes(title_text="Runs Scored per Over", secondary_y=True)
        fig.update_layout(yaxis2_range=[0,40])
        fig.update_yaxes(secondary_y=True, showgrid=False)
        st.plotly_chart(fig)

        st.markdown("**Score Predictions Tabulated**")
        cols_to_display = ['Over','Prediction','Current RunRate','Projected RunRate']
        st.write(response.data.loc[3:,cols_to_display])

else:
    st.markdown("This feature is not avialable in streamlit online deployment and advised to run a local copy of this application for execution.")

    st.markdown("It is required to install [Streamlit](https://streamlit.io/) on your device to run this feature locally.")
    st.markdown("Refer the streamlit documentation for installation process depending on your operating system.")
    st.markdown("1. [Windows](docs.streamlit.io/library/get-started/installation#install-streamlit-on-windows)")
    st.markdown("2. [MacOS/Linux](docs.streamlit.io/library/get-started/installation#install-streamlit-on-macoslinux)")

    st.markdown("Clone this application from github using")
    code1 = '''git clone github.com/navindu-ds/T20-Cricket-Score-Predictor'''
    st.code(code1, language='terminal')

    st.markdown("Use the following code in the streamlit supported environment to run the application")
    code2 = '''python -m streamlit run App.py'''
    st.code(code2, language='terminal')