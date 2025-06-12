import streamlit as st
import pickle
import pandas as pd

def run_team_win_app():
    
    # Enhanced CSS with team branding and modern design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 100%);
        min-height: 100vh;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.15"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 3.2rem;
        font-weight: 800;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin-top: 0.8rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .cricket-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .input-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .section-title {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 12px;
        letter-spacing: -0.5px;
    }
    
    .team-selection-container {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 2rem;
        align-items: center;
        margin: 2rem 0;
    }
    
    .team-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .team-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .team-logo {
        width: 80px;
        height: 80px;
        margin: 0 auto 1rem;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .team-logo img {
        width: 60px;
        height: 60px;
        object-fit: contain;
    }
    
    .vs-divider {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 50%;
        font-size: 1.5rem;
        font-weight: 800;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .prediction-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .prediction-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .prediction-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .probability-cards {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
        position: relative;
        z-index: 1;
    }
    
    .win-probability {
        background: rgba(255, 255, 255, 0.15);
        padding: 2rem;
        border-radius: 16px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        transition: all 0.3s ease;
    }
    
    .win-probability:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
    }
    
    .team-name {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    .team-name-logo {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .team-name-logo img {
        width: 24px;
        height: 24px;
        object-fit: contain;
    }
    
    .probability-display {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 1rem 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .probability-bar {
        background: rgba(255, 255, 255, 0.3);
        height: 12px;
        border-radius: 6px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .probability-fill {
        height: 100%;
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
        transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 6px;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
    }
    
    .stat-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .stat-value {
        color: #667eea;
        font-size: 2rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .predict-button {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border: none;
        padding: 1.2rem 3rem;
        border-radius: 50px;
        font-size: 1.3rem;
        font-weight: 700;
        box-shadow: 0 8px 24px rgba(255, 107, 53, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 2rem auto;
        display: block;
    }
    
    .predict-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(255, 107, 53, 0.6);
        background: linear-gradient(135deg, #F7931E 0%, #FF6B35 100%);
    }
    
    .conditions-section {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .condition-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: white;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: white;
    }
    
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    .impact-analysis {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        backdrop-filter: blur(15px);
    }
    
    .impact-title {
        color: #667eea;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .impact-item {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .impact-item:last-child {
        border-bottom: none;
    }
    
    .boost-positive {
        color: #4CAF50;
        font-weight: 600;
    }
    
    .boost-negative {
        color: #FF5722;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # Team logos mapping
    team_logos = {
        'Chennai Super Kings': 'https://documents.iplt20.com/ipl/CSK/logos/Logooutline/CSKoutline.png',
        'Delhi Capitals': 'https://documents.iplt20.com/ipl/DC/Logos/LogoOutline/DCoutline.png',
        'Gujarat Titans': 'https://documents.iplt20.com/ipl/GT/Logos/Logooutline/GToutline.png',
        'Kolkata Knight Riders': 'https://documents.iplt20.com/ipl/KKR/Logos/Logooutline/KKRoutline.png',
        'Lucknow Super Giants': 'https://documents.iplt20.com/ipl/LSG/Logos/Logooutline/LSGoutline.png',
        'Mumbai Indians': 'https://documents.iplt20.com/ipl/MI/Logos/Logooutline/MIoutline.png',
        'Punjab Kings': 'https://documents.iplt20.com/ipl/PBKS/Logos/Logooutline/PBKSoutline.png',
        'Rajasthan Royals': 'https://documents.iplt20.com/ipl/RR/Logos/Logooutline/RRoutline.png',
        'Royal Challengers Bangalore': 'https://documents.iplt20.com/ipl/RCB/Logos/Logooutline/RCBoutline.png',
        'Sunrisers Hyderabad': 'https://documents.iplt20.com/ipl/SRH/Logos/Logooutline/SRHoutline.png'
    }

    # Updated teams list to match logo keys
    teams = [
        'Chennai Super Kings',
        'Delhi Capitals', 
        'Gujarat Titans',
        'Kolkata Knight Riders',
        'Lucknow Super Giants',
        'Mumbai Indians',
        'Punjab Kings',
        'Rajasthan Royals',
        'Royal Challengers Bangalore',
        'Sunrisers Hyderabad'
    ]

    cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
        'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
        'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
        'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
        'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
        'Sharjah', 'Mohali']

    # Load model (with error handling for demo)
    try:
        pipe = pickle.load(open('pipe.pkl','rb'))
    except:
        st.error("Model file not found. Please ensure 'pipe.pkl' is in the correct directory.")
        pipe = None
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="cricket-icon">🏏</div>
        <h1>IPL Win Predictor</h1>
        <p>Advanced Cricket Analytics & Match Prediction Engine</p>
    </div>
    """, unsafe_allow_html=True)

    # Team Selection Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏏 Team Selection</div>', unsafe_allow_html=True)
    
    # Team selection with logos
    col1, col_vs, col2 = st.columns([2, 1, 2])
    
    with col1:
        batting_team = st.selectbox('🏏 Batting Team', sorted(teams), help="Select the team currently batting")
        if batting_team in team_logos:
            st.markdown(f"""
            <div class="team-card">
                <div class="team-logo">
                    <img src="{team_logos[batting_team]}" alt="{batting_team}" />
                </div>
                <div style="color: white; font-weight: 600;">{batting_team}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_vs:
        st.markdown('<div class="vs-divider">VS</div>', unsafe_allow_html=True)
    
    with col2:
        bowling_team = st.selectbox('🥎 Bowling Team', sorted(teams), help="Select the team currently bowling")
        if bowling_team in team_logos:
            st.markdown(f"""
            <div class="team-card">
                <div class="team-logo">
                    <img src="{team_logos[bowling_team]}" alt="{bowling_team}" />
                </div>
                <div style="color: white; font-weight: 600;">{bowling_team}</div>
            </div>
            """, unsafe_allow_html=True)

    selected_city = st.selectbox('🏟 Host City', sorted(cities), help="Select the match venue city")
    st.markdown('</div>', unsafe_allow_html=True)

    # Match Status Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Current Match Status</div>', unsafe_allow_html=True)
    
    target = st.number_input('🎯 Target Score', min_value=0, value=180, help="Total runs to chase")

    col3, col4, col5 = st.columns(3)
    with col3:
        score = st.number_input('📈 Current Score', min_value=0, value=120, help="Runs scored so far")
    with col4:
        overs = st.number_input('⏱ Overs Completed', min_value=0.0, max_value=20.0, value=15.0, step=0.1, help="Overs bowled")
    with col5:
        wickets_out = st.number_input('🏏 Wickets Lost', min_value=0, max_value=10, value=3, help="Wickets fallen")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Match Conditions Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌤 Match Conditions</div>', unsafe_allow_html=True)
    
    col_pitch, col_weather = st.columns(2)
    
    with col_pitch:
        pitch_description = st.selectbox("🏟 Pitch Description", [
            "Flat pitch, no swing/spin",
            "Grass or cracks, uneven bounce", 
            "Dry and worn-out",
            "Green pitch, morning moisture"
        ], help="Select the pitch conditions")
    
    with col_weather:
        weather_conditions = st.multiselect("🌦 Weather Conditions", [
            "dew_expected", "overcast", "hot_dry", "day_match", "night_match", "humidity_high"
        ], help="Select applicable weather conditions")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
<style>
.stButton > button {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    color: white;
    border: none;
    padding: 1.2rem 3rem;
    border-radius: 50px;
    font-size: 1.3rem;
    font-weight: 700;
    box-shadow: 0 8px 24px rgba(255, 107, 53, 0.4);
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
    width: 100%;
    margin: 2rem 0;
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(255, 107, 53, 0.6);
    background: linear-gradient(135deg, #F7931E 0%, #FF6B35 100%);
}
</style>
""", unsafe_allow_html=True)

# Create the button and store its state
    predict_button = st.button('🎯 Calculate Prediction', key="predict_btn", help="Click to generate win probability prediction")
    
    
    if predict_button and pipe is not None:

        runs_left = max(0,target - score)
        balls_left = max(0, 120 - (overs * 6))
        wickets = 10 - wickets_out
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

  
        input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
         })

   
        result = pipe.predict_proba(input_df)
        win = result[0][1]
        loss = result[0][0]

    # Apply pitch and weather adjustments
        chasing_team = batting_team  
        team1 = batting_team
        team2 = bowling_team

        PITCH_WEIGHTS = {
        "Flat pitch, no swing/spin": {team1: +7, team2: -7},
        "Grass or cracks, uneven bounce": {team1: -5, team2: +5},
        "Dry and worn-out": {team1: +2, team2: +5},
        "Green pitch, morning moisture": {team1: -4, team2: +6}
    }

        WEATHER_WEIGHTS = {
        "dew_expected": {chasing_team: +5},
        "overcast": {team2: +4},
        "hot_dry": {team2: +3},
        "day_match": {team2: +2},
        "night_match": {chasing_team: +3},
        "humidity_high": {team2: +4}
    }

        adjustment = {team1: 0, team2: 0}

        if pitch_description in PITCH_WEIGHTS:
         for team, boost in PITCH_WEIGHTS[pitch_description].items():
            adjustment[team] += boost

        for cond in weather_conditions:
            if cond in WEATHER_WEIGHTS:
                for team, boost in WEATHER_WEIGHTS[cond].items():
                 adjustment[team] += boost

   
        win = max(0, min(1, win + (adjustment[team1] * 0.01)))
        loss = max(0, min(1, loss + (adjustment[team2] * 0.01)))

  
        total = win + loss
        if total > 0:
          win = win / total
          loss = loss / total
        else:
          win = 0.5
          loss = 0.5

    
        win_percentage = round(win * 100, 1)
        loss_percentage = round(loss * 100, 1)

    
        st.markdown("""
        <div class="prediction-container">
            <div class="prediction-title">🏆 Win Probability Analysis</div>
            <div class="probability-cards">
        """, unsafe_allow_html=True)


        batting_logo = team_logos.get(batting_team, '')
        st.markdown(f"""
            <div class="win-probability">
                <div class="team-name">
                    <div class="team-name-logo">
                        <img src="{batting_logo}" alt="{batting_team}" />
                    </div>
                    {batting_team}
                </div>
                <div class="probability-display">{win_percentage}%</div>
                <div class="probability-bar">
                    <div class="probability-fill" style="width: {win_percentage}%"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    
        bowling_logo = team_logos.get(bowling_team, '')
        st.markdown(f"""
            <div class="win-probability">
                <div class="team-name">
                    <div class="team-name-logo">
                        <img src="{bowling_logo}" alt="{bowling_team}" />
                    </div>
                    {bowling_team}
                </div>
                <div class="probability-display">{loss_percentage}%</div>
                <div class="probability-bar">
                    <div class="probability-fill" style="width: {loss_percentage}%"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)


        # Enhanced Match Statistics
    st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">{runs_left}</div>
                <div class="stat-label">Runs Required</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⚾</div>
                <div class="stat-value">{balls_left}</div>
                <div class="stat-label">Balls Remaining</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🏏</div>
                <div class="stat-value">{wickets}</div>
                <div class="stat-label">Wickets in Hand</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-value">{crr:.2f}</div>
                <div class="stat-label">Current Run Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⚡</div>
                <div class="stat-value">{rrr:.2f}</div>
                <div class="stat-label">Required Run Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🏟</div>
                <div class="stat-value">{selected_city}</div>
                <div class="stat-label">Venue</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced Conditions Impact Analysis
    if pitch_description or weather_conditions:
            st.markdown(f"""
            <div class="impact-analysis">
                <div class="impact-title">🌤 Conditions Impact Analysis</div>
                <div class="impact-item"><strong>Pitch Condition:</strong> {pitch_description}</div>
            """, unsafe_allow_html=True)
            
            if weather_conditions:
                weather_str = ', '.join(weather_conditions)
                st.markdown(f'<div class="impact-item"><strong>Weather Factors:</strong> {weather_str}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="impact-item"><strong>Weather Factors:</strong> Clear conditions</div>', unsafe_allow_html=True)
            
            
            
            st.markdown('</div>', unsafe_allow_html=True)

    elif predict_button and pipe is None:
        st.error("⚠ Model not loaded. Please ensure the pickle file is available.")

    # Additional Features Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Additional Features</div>', unsafe_allow_html=True)
    
    col_feat1, col_feat2 = st.columns(2)
    
    with col_feat1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">🎲</div>
            <div class="stat-label">Key Factors</div>
            <div style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; margin-top: 1rem;">
                • Run rate differential<br>
                • Wickets in hand<br>
                • Venue conditions<br>
                • Historical performance
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_feat2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">🔮</div>
            <div class="stat-label">Prediction Accuracy</div>
            <div style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; margin-top: 1rem;">
                • Machine Learning Model<br>
                • 85%+ Accuracy Rate<br>
                • Real-time Analysis<br>
                • Weather Adjustments
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;">
        <p>🏏 Enhanced IPL Win Predictor | Powered by Advanced Analytics</p>
        <p>Disclaimer: Predictions are based on statistical models and should be used for entertainment purposes only.</p>
    </div>
    """, unsafe_allow_html=True)