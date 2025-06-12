import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

# Load dataset
df = pd.read_csv(r"C:\Users\om718\OneDrive\Desktop\New folder (4)\ipl_batsmen_current_players_no_team.csv")

# Convert categorical columns to category type and encode them
categorical_cols = ["Player", "Opponent Team", "Venue"]
label_encoders = {}
for col in categorical_cols:
    df[col] = df[col].astype("category")  # Convert to categorical
    label_encoders[col] = {category: code for code, category in enumerate(df[col].cat.categories)}  # Save mapping
    df[col] = df[col].cat.codes  # Encode as integer

# Ensure 'Team' is also encoded if it exists
if "Team" in df.columns:
    df["Team"] = df["Team"].astype("category").cat.codes

# Define features and target
X = df.drop(columns=["Predicted Runs"])
y = df["Predicted Runs"]

# Standardize numerical features
scaler = StandardScaler()
numeric_cols = ["Matches Played", "Avg Runs per Match", "Strike Rate", "Batting Position", "Previous Match Runs", "Form (Last 5 Innings Avg.)"]
X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print feature count before training
print("Training feature count:", X_train.shape[1])

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7]
}

grid_search = GridSearchCV(XGBRegressor(random_state=42), param_grid, cv=3, scoring='r2', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best model from GridSearchCV
best_model = grid_search.best_estimator_

# Evaluate model performance
y_pred = best_model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"Model Performance:\nR2 Score: {r2:.4f}\nMean Absolute Error: {mae:.4f}\nMean Squared Error: {mse:.4f}")

# Save model and preprocessors
with open("model.pkl", "wb") as file:
    pickle.dump(best_model, file)
with open("label_encoders.pkl", "wb") as file:
    pickle.dump(label_encoders, file)
with open("scaler.pkl", "wb") as file:
    pickle.dump(scaler, file)

print("Model training complete. Best parameters found and files saved!")
