import streamlit as st
from team_win_predictor import run_team_win_app
from batsman_run_predictor import run_batsman_run_app

st.sidebar.title("IPL Prediction Navigation")
app_mode = st.sidebar.selectbox("Choose an app", ["Team Win Predictor", "Batsman Run Predictor"])

if app_mode == "Team Win Predictor":
    run_team_win_app()
elif app_mode == "Batsman Run Predictor":
    run_batsman_run_app()

