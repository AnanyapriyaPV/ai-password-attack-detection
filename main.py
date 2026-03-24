import random
import time
import pandas as pd
from collections import deque

from auth.user_manager import User
from auth.session_auth import authenticate_login
from attacks.attack_simulator import AttackSimulator, load_rockyou
from risk_prediction.predict_risk import load_model
from auth.vulnerability import calculate_entropy

from adaptive_decision.decision_engine import adaptive_decision
from adaptive_decision.monitoring_logger import log_event


# ----------------------------
# Setup
# ----------------------------

print("\nAI-Powered Login Security System\n")

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

wordlist = load_rockyou("rockyou.txt", limit=10000)
model = load_model()
simulator = AttackSimulator(users, wordlist)

# ----------------------------
# HISTORY STORAGE
# ----------------------------

login_history = {u.user_id: deque(maxlen=10) for u in users}
rolling_window = {u.user_id: deque(maxlen=5) for u in users}


# ----------------------------
# User Input
# ----------------------------

print("Choose Mode:")
print("1 → Legitimate Login")
print("2 → Attack Simulation")

mode = input("Enter choice: ")

events = []

# ----------------------------
# AUTHENTICATION
# ----------------------------

if mode == "1":

    user = random.choice(users)
    password = user.password
    attack_type = "legitimate"

    auth_result = authenticate_login(user, password)
    events = [(user, password, auth_result)]


elif mode == "2":

    print("\nChoose Attack Type:")
    print("1 → Dictionary")
    print("2 → Rapid Burst")
    print("3 → Low and Slow")
    print("4 → Replay")

    attack_choice = input("Enter choice: ")

    if attack_choice == "1":
        simulator.run_dictionary_attack(count=5)
        attack_type = "dictionary"

    elif attack_choice == "2":
        simulator.run_rapid_burst(5)
        attack_type = "rapid_burst"

    elif attack_choice == "3":
        simulator.run_low_and_slow(5)
        attack_type = "low_and_slow"

    elif attack_choice == "4":
        simulator.run_replay_attack()
        attack_type = "replay"

    else:
        print("Invalid choice")
        exit()

    sim_events = simulator.get_events()[-5:]

    for event in sim_events:
        password = event["password_attempt"]
        user_id = event["user_id"]
        user = next(u for u in users if u.user_id == user_id)

        auth_result = authenticate_login(user, password)
        events.append((user, password, auth_result))

else:
    print("Invalid input")
    exit()


# ----------------------------
# PROCESS EVENTS
# ----------------------------

base_time = time.time()

for user, password, auth_result in events:

    # ----------------------------
    # SIMULATED TIME GAP (KEY FIX)
    # ----------------------------

    if attack_type == "rapid_burst":
        gap = random.uniform(0.01, 0.05)

    elif attack_type == "low_and_slow":
        gap = random.uniform(2, 5)

    elif attack_type == "dictionary":
        gap = random.uniform(0.2, 1)

    else:  # legit / replay
        gap = random.uniform(1, 3)

    base_time += gap
    current_time = base_time

    # ----------------------------
    # TIME GAP NORMALIZATION
    # ----------------------------

    login_history[user.user_id].append(current_time)
    times = list(login_history[user.user_id])

    if len(times) >= 2:
        gaps = [times[i] - times[i-1] for i in range(1, len(times))]
        avg_gap = sum(gaps) / len(gaps)
        last_gap = gaps[-1]

        normalized_gap = min(last_gap / (avg_gap + 1e-5), 5)
    else:
        normalized_gap = 1

    # ----------------------------
    # ROLLING ATTEMPTS (FIXED)
    # ----------------------------

    rolling_window[user.user_id].append(auth_result["failed_attempts"])
    rolling_attempts = sum(rolling_window[user.user_id])

    # ----------------------------
    # FEATURES
    # ----------------------------

    entropy = calculate_entropy(password) / 100
    failed_attempts = min(auth_result["failed_attempts"] / 5, 1)
    vulnerability = auth_result["vulnerability_score"]
    dictionary_flag = 1 if password in wordlist else 0

    # Replay signal (simple heuristic)
    replay_flag = 1 if attack_type == "replay" else 0

    # ----------------------------
    # FEATURE VECTOR
    # ----------------------------

    feature_vector = [
        entropy,
        failed_attempts,
        vulnerability,
        normalized_gap,
        rolling_attempts,
        dictionary_flag + replay_flag   # merged signal
    ]

    # ----------------------------
    # PREDICTION
    # ----------------------------

    feature_df = pd.DataFrame([feature_vector], columns=[
        "password_entropy",
        "failed_attempts",
        "vulnerability_score",
        "time_gap",
        "rolling_attempts",
        "dictionary_flag"
    ])

    risk_prob = model.predict_proba(feature_df)[0][1]

    decision = adaptive_decision(risk_prob)

    # ----------------------------
    # LOGGING
    # ----------------------------

    event = {
        "timestamp": int(current_time),
        "user_id": user.user_id,
        "attack_type": attack_type,
        "risk_score": float(risk_prob),
        "decision": decision
    }

    log_event(event)

    # ----------------------------
    # OUTPUT
    # ----------------------------

    print("\n--- EVENT ---")
    print("User:", user.user_id)
    print("Attack:", attack_type)
    print("Gap:", round(gap, 3))
    print("Norm Gap:", round(normalized_gap, 3))
    print("Features:", feature_vector)
    print("Risk:", round(risk_prob, 3))
    print("Decision:", decision)