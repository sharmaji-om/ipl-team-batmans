import pickle
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBRegressor

# Load model and preprocessors
with open("model.pkl", "rb") as file:
    model = pickle.load(file)
with open("scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

# Define column order
feature_columns =  ['Player', 'Matches Played', 'Avg Runs per Match', 'Strike Rate', 'Batting Position', 'Opponent Team', 'Venue', 'Previous Match Runs', 'Form (Last 5 Innings Avg.)']
# Define numeric columns
numeric_cols = ["Matches Played", "Avg Runs per Match", "Strike Rate", "Batting Position", "Previous Match Runs", "Form (Last 5 Innings Avg.)"]

# Load dataset to fit label encoders
dataset = pd.read_csv(r"C:\Users\om718\OneDrive\Desktop\New folder (4)\ipl_batsmen_current_players_no_team.csv")
categorical_cols = ["Player", "Opponent Team", "Venue"]
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    dataset[col] = dataset[col].astype(str)
    dataset[col] = le.fit_transform(dataset[col])
    label_encoders[col] = le

def inverse_transform(column, value):
    if column in label_encoders:
        return label_encoders[column].inverse_transform([value])[0]
    return value

# Function to preprocess new input data
def preprocess_input(input_data, label_encoders, scaler):
    for col in categorical_cols:
        if col in input_data.columns:
            if col in label_encoders:
                input_data[col] = input_data[col].apply(lambda x: label_encoders[col].transform([x])[0] if x in label_encoders[col].classes_ else -1)
            else:
                input_data[col] = -1  # Default unknown category encoding
    
    # Ensure all numeric columns exist and are of correct type
    for col in numeric_cols:
        if col not in input_data.columns:
            input_data[col] = 0  # Default value
    
    # Convert numeric columns to float and scale them
    input_data[numeric_cols] = scaler.transform(input_data[numeric_cols].astype(float))  
    
    return input_data

# Streamlit UI
st.title("IPL Batsman Performance Prediction By Om sharma , Anand Pandit & Vasudev Kumar")

# User inputs
player_name = st.selectbox("Player Name", label_encoders["Player"].inverse_transform(range(len(label_encoders["Player"].classes_))))
opponent_name = st.selectbox("Opponent Team", label_encoders["Opponent Team"].inverse_transform(range(len(label_encoders["Opponent Team"].classes_))))
venue_name = st.selectbox("Venue", label_encoders["Venue"].inverse_transform(range(len(label_encoders["Venue"].classes_))))
matches_played = st.number_input("Matches Played", min_value=0, step=1)
avg_runs = st.number_input("Average Runs per Match")
strike_rate = st.number_input("Strike Rate")
batting_position = st.number_input("Batting Position", min_value=1, max_value=11, step=1)
previous_match_runs = st.number_input("Previous Match Runs")
form_avg = st.number_input("Form (Last 5 Innings Avg.)")

if st.button("Predict Runs"):
    # Convert categorical inputs to encoded values
    player = label_encoders["Player"].transform([player_name])[0]
    opponent = label_encoders["Opponent Team"].transform([opponent_name])[0]
    venue = label_encoders["Venue"].transform([venue_name])[0]
    
    # Create input DataFrame with the correct column order
    input_data = pd.DataFrame([[player, opponent, venue, matches_played, avg_runs, strike_rate, batting_position, previous_match_runs, form_avg]],
                              columns=feature_columns)
    
    # Preprocess input
    try:
        input_data = preprocess_input(input_data, label_encoders, scaler)
        input_data = input_data[feature_columns]  # Ensure correct column order
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted Runs: {prediction:.2f}")
        
        # Display inverse transformed values
        st.write("### Input Details:")
        st.write(f"**Player:** {player_name}")
        st.write(f"**Opponent Team:** {opponent_name}")
        st.write(f"**Venue:** {venue_name}")
    except Exception as e:
        st.error(f"Error in prediction: {e}")
