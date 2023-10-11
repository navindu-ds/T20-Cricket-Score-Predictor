import streamlit as st

# Initialization
st.session_state = False

st.markdown("# T20 Cricket Score Predictor App 🏏")
st.sidebar.markdown("# The T20 Cricket Score Predictor App 🏏")
st.sidebar.markdown("**source code on [github](https://github.com/navindu-ds/T20-Cricket-Score-Predictor)**")
st.sidebar.markdown("*Currently* modelled only for **1st Innings** predictions")

st.markdown("## Click [here](Predictor) for a quick prediction!")

st.markdown("### Run the application locally to use all features")

st.markdown("### Instructions to run Application Locally")

st.markdown("It is required to install [Streamlit](https://streamlit.io/) on your device to run all features application locally.")
st.markdown("Refer the streamlit documentation for installation process depending on your operating system.")
st.markdown("1. [Windows](docs.streamlit.io/library/get-started/installation#install-streamlit-on-windows)")
st.markdown("2. [MacOS/Linux](docs.streamlit.io/library/get-started/installation#install-streamlit-on-macoslinux)")

st.markdown("Clone this application from github using")
code1 = '''git clone github.com/navindu-ds/T20-Cricket-Score-Predictor'''
st.code(code1, language='terminal')

st.markdown("Use the following code in the streamlit supported environment to run the application")
code1 = '''python -m streamlit run App.py'''
st.code(code1, language='terminal')