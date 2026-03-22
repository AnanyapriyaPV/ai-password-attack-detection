from feature_extraction import extract_features
from train_model import train_model
from predict_risk import load_model
import pandas as pd

# Load dataset
X, y = extract_features("login_events.csv")

# Train model
model = train_model(X, y)

# Load trained model
model = load_model()

# Create a SAFE login example (low risk values)
sample = pd.DataFrame([[1.0, 0, 0.1, 5, 1]],
columns=[
    "password_entropy",
    "failed_attempts",
    "vulnerability_score",
    "time_gap",
    "rolling_attempts"
])

# Predict
result = model.predict(sample)[0]

print("Output:", result)