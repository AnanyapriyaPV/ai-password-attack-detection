import pandas as pd
import random

from feature_extraction import extract_features
from train_model import train_model
from predict_risk import load_model, predict_risk

from auth.user_manager import User
from attacks.attack_simulator import AttackSimulator, load_rockyou
from auth.session_auth import authenticate_login

# ---------------------------
# Setup Users + Wordlist
# ---------------------------

users = [
    User("alice", "admin123"),
    User("bob", "Secure@456"),
    User("charlie", "Qwerty@789"),
    User("david", "StrongPass!99"),
    User("eva", "letmein123"),
    User("frank", "T!gerLily#2026"),
    User("grace", "C0smic$Ray_88"),
    User("henry", "BlueSky!7Clouds"),
    User("isabel", "Quantum@Leap42"),
    User("jack", "Sun&Moon_2025!"),
    User("karen", "IronHorse#77$"),
    User("leo", "Phoenix_Fire!123"),
    User("mia", "OceanWave$456!"),
    User("nathan", "Galaxy@Storm99"),
    User("olivia", "ShadowWolf!2026")
]

wordlist = load_rockyou("rockyou.txt", limit=5000)
simulator = AttackSimulator(users, wordlist)

# ---------------------------
# Train Model from Dataset
# ---------------------------

X, y = extract_features("login_events.csv")
model = train_model(X, y)

# Load trained model
model = load_model()

# ---------------------------
# SELECT TEST MODE
# ---------------------------

mode = input("Choose mode (legit / attack): ").strip().lower()

if mode == "legit":
    user = random.choice(users)
    password = user.password
    result = authenticate_login(user, password)
    password_attempt = password
    attack_type = "legitimate"

else:
    user = random.choice(users)
    password_attempt = random.choice(wordlist)
    result = authenticate_login(user, password_attempt)
    attack_type = "attack"

# ---------------------------
# FEATURE VECTOR CREATION
# ---------------------------

feature_vector = [
    len(password_attempt),                    # entropy proxy (simplified)
    result["failed_attempts"],
    result["vulnerability_score"],
    1,                                       # dummy time_gap
    result["failed_attempts"],                # rolling attempts proxy
    1 if password_attempt in wordlist else 0  # dictionary flag
]

# ---------------------------
# PREDICT RISK
# ---------------------------

prediction = predict_risk(model, feature_vector)

print("\n--- ML OUTPUT ---")
print("User:", user.user_id)
print("Attack Type:", attack_type)
print("Prediction (0=Safe,1=Attack):", prediction)

# Return for Module 4 use
output = {
    "user_id": user.user_id,
    "risk_score": float(prediction)  # convert to numeric
}