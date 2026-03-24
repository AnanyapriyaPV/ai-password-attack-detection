print("Running Integrated System...")

from adaptive_decision.decision_engine import adaptive_decision
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
# LOG EVENT
# ---------------------------

event = {
    "user_id": user_id,
    "risk_score": round(risk_score, 2),
    "decision": decision
}

log_event(event)

# ---------------------------
# PRINT OUTPUT
# ---------------------------

print("\n--- FINAL DECISION ---")
print("User:", user_id)
print("Risk Score:", round(risk_score, 2))
print("Decision:", decision)