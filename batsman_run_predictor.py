import pickle
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBRegressor

def run_batsman_run_app():
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 50%, #FFD23F 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .authors {
        color: white;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-style: italic;
    }
    
    .input-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #FF6B35;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .prediction-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .prediction-result h2 {
        margin: 0;
        font-size: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .context-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 0.8rem 0;
        box-shadow: 0 6px 15px rgba(255, 107, 53, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 3px solid #FF6B35;
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        border: none;
        color: white;
        text-align: center;
    }
    
    .info-box h3 {
        color: white;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .step-item {
        background: rgba(255, 255, 255, 0.15);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .step-number {
        display: inline-block;
        background: #FFD23F;
        color: #333;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        text-align: center;
        line-height: 30px;
        font-weight: bold;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏏 IPL Batsman Performance Predictor</h1>
        <div class="authors">By Om Sharma, Anand Pandit & Vasudev Kumar</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load models (keeping original logic)
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)
    with open("scaler.pkl", "rb") as file:
        scaler = pickle.load(file)

    # Feature columns in the exact order expected by the model
    feature_columns = ['Player', 'Matches Played', 'Avg Runs per Match', 'Strike Rate', 
                       'Batting Position', 'Opponent Team', 'Venue', 'Previous Match Runs', 
                       'Form (Last 5 Innings Avg.)']
    
    numeric_cols = ["Matches Played", "Avg Runs per Match", "Strike Rate", 
                    "Batting Position", "Previous Match Runs", "Form (Last 5 Innings Avg.)"]
    url =  "https://raw.githubusercontent.com/sharmaji-om/ipl-team-batmans/main/ipl_batsmen_current_players_no_team.csv"

    dataset =  pd.read_csv(url) 
    categorical_cols = ["Player", "Opponent Team", "Venue"]
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        dataset[col] = dataset[col].astype(str)
        dataset[col] = le.fit_transform(dataset[col])
        label_encoders[col] = le

    def preprocess_input(input_data, label_encoders, scaler):
        for col in categorical_cols:
            if col in input_data.columns:
                if col in label_encoders:
                    input_data[col] = input_data[col].apply(
                        lambda x: label_encoders[col].transform([x])[0] 
                        if x in label_encoders[col].classes_ else -1)
                else:
                    input_data[col] = -1
        
        for col in numeric_cols:
            if col not in input_data.columns:
                input_data[col] = 0

        input_data[numeric_cols] = scaler.transform(input_data[numeric_cols].astype(float))  
        return input_data

    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Player Information Section
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("### 👤 Player Information")
        
        player_name = st.selectbox(
            "🏏 Player Name", 
            label_encoders["Player"].inverse_transform(range(len(label_encoders["Player"].classes_))),
            help="Select the batsman whose performance you want to predict"
        )
        
        col_team, col_venue = st.columns(2)
        with col_team:
            opponent_name = st.selectbox(
                "🆚 Opponent Team", 
                label_encoders["Opponent Team"].inverse_transform(range(len(label_encoders["Opponent Team"].classes_))),
                help="Select the opposing team"
            )
        
        with col_venue:
            venue_name = st.selectbox(
                "🏟 Venue", 
                label_encoders["Venue"].inverse_transform(range(len(label_encoders["Venue"].classes_))),
                help="Select the match venue"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Performance Statistics Section
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("### 📊 Performance Statistics")
        
        col_stats1, col_stats2 = st.columns(2)
        with col_stats1:
            matches_played = st.number_input("🎯 Matches Played", min_value=0, step=1, help="Total matches played by the player")
            avg_runs = st.number_input("📈 Average Runs per Match", help="Player's batting average")
            strike_rate = st.number_input("⚡ Strike Rate", help="Player's strike rate")
        
        with col_stats2:
            batting_position = st.number_input("🔢 Batting Position", min_value=1, max_value=11, step=1, help="Player's batting order position")
            previous_match_runs = st.number_input("🏃 Previous Match Runs", help="Runs scored in the last match")
            form_avg = st.number_input("📊 Form (Last 5 Innings Avg.)", help="Average runs in last 5 innings")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Match Conditions Section
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("### 🌤 Match Conditions")
        
        pitch_description = st.selectbox("🏟 Pitch Description", [
            "Flat pitch, no swing/spin",
            "Grass or cracks, uneven bounce",
            "Dry and worn-out",
            "Green pitch, morning moisture"
        ], help="Select the pitch conditions")
        
        weather_conditions = st.multiselect("🌦 Weather Conditions", [
            "dew_expected", "overcast", "hot_dry", "day_match", "night_match", "humidity_high"
        ], help="Select applicable weather conditions")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Prediction Button
        predict_button = st.button("🎯 Predict Performance", key="predict_btn")

    with col2:
        # Information Panel
        st.markdown("""
        <div class="info-box">
            <h3>✨ How to Use</h3>
            <div class="step-item">
                <span class="step-number">1</span>
                <strong>Pick Your Player</strong><br>
                Choose batsman & opponent team
            </div>
            <div class="step-item">
                <span class="step-number">2</span>
                <strong>Enter Stats</strong><br>
                Add performance numbers
            </div>
            <div class="step-item">
                <span class="step-number">3</span>
                <strong>Set Conditions</strong><br>
                Select pitch & weather
            </div>
            <div class="step-item">
                <span class="step-number">4</span>
                <strong>Get Prediction</strong><br>
                Click predict button
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Stats Display
        if 'player_name' in locals():
            st.markdown(f"""
            <div class="metric-card">
                <h4>Selected Player</h4>
                <h3>{player_name}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        if 'opponent_name' in locals():
            st.markdown(f"""
            <div class="metric-card">
                <h4>vs</h4>
                <h3>{opponent_name}</h3>
            </div>
            """, unsafe_allow_html=True)

    # Prediction Results
    if predict_button:
        try:
            # Original prediction logic
            player = label_encoders["Player"].transform([player_name])[0]
            opponent = label_encoders["Opponent Team"].transform([opponent_name])[0]
            venue = label_encoders["Venue"].transform([venue_name])[0]

            # Create input data in the correct order expected by the model
            input_data = pd.DataFrame([[player, matches_played, avg_runs, strike_rate, 
                                        batting_position, opponent, venue, previous_match_runs, form_avg]],
                                      columns=feature_columns)

            input_data = preprocess_input(input_data, label_encoders, scaler)
            input_data = input_data[feature_columns]
            predicted_runs = model.predict(input_data)[0]

            # Pitch adjustments (original logic)
            pitch_adjustment = 0
            if pitch_description == "Flat pitch, no swing/spin":
                pitch_adjustment += np.random.randint(10, 16)
            elif pitch_description in ["Grass or cracks, uneven bounce", "Green pitch, morning moisture"]:
                predicted_runs *= 0.95

            if "dew_expected" in weather_conditions or "hot_dry" in weather_conditions:
                pitch_adjustment += 3
            if "overcast" in weather_conditions:
                predicted_runs *= 0.97

            final_prediction = predicted_runs + pitch_adjustment

            # Enhanced results display
            st.markdown(f"""
            <div class="prediction-result">
                <h2>🎯 Predicted Runs: {final_prediction:.0f}</h2>
                <p>Based on current form and match conditions</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Match context with better styling
            st.markdown('<div class="context-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Match Summary")
            
            col_context1, col_context2 = st.columns(2)
            with col_context1:
                st.markdown(f"🏏 Player:** {player_name}")
                st.markdown(f"🆚 Opponent:** {opponent_name}")
                st.markdown(f"🏟 Venue:** {venue_name}")
            
            with col_context2:
                st.markdown(f"🌱 Pitch:** {pitch_description}")
                st.markdown(f"🌤 Weather:** {', '.join(weather_conditions) if weather_conditions else 'Clear conditions'}")
                st.markdown(f"📊 Form:** {form_avg:.1f} runs avg")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Performance insights
            with st.expander("📈 Performance Insights"):
                col_insight1, col_insight2, col_insight3 = st.columns(3)
                
                with col_insight1:
                    st.metric("Strike Rate", f"{strike_rate:.1f}", help="Runs per 100 balls")
                
                with col_insight2:
                    st.metric("Batting Average", f"{avg_runs:.1f}", help="Average runs per match")
                
                with col_insight3:
                    st.metric("Recent Form", f"{form_avg:.1f}", help="Last 5 innings average")

        except Exception as e:
            st.error(f"❌ Error in prediction: {e}")
            st.info("Please check your input values and try again.")





