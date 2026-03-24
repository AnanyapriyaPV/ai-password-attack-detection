print("Running Integrated System...")

from adaptive_decision.decision_engine import adaptive_decision
from adaptive_decision.slow_attack_detector import detect_slow_attack
from adaptive_decision.monitoring_logger import log_event

# Import ML pipeline
from risk_prediction.main_pipeline import output

# ---------------------------
# GET ML OUTPUT
# ---------------------------

user_id = output["user_id"]
risk_score = output["risk_score"]

# ---------------------------
# ADAPTIVE DECISION
# ---------------------------

decision = adaptive_decision(risk_score)

# ---------------------------
# SLOW ATTACK DETECTION
# ---------------------------

slow_attack = detect_slow_attack(user_id)

# ---------------------------
# LOG EVENT
# ---------------------------

event = {
    "user_id": user_id,
    "risk_score": round(risk_score, 2),
    "decision": decision,
    "slow_attack_detected": slow_attack
}

log_event(event)

# ---------------------------
# PRINT OUTPUT
# ---------------------------

print("\n--- FINAL DECISION ---")
print("User:", user_id)
print("Risk Score:", round(risk_score, 2))
print("Decision:", decision)
print("Slow Attack:", slow_attack)