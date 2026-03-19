print("Running Module 4...")

import random
from adaptive_decision.decision_engine import adaptive_decision
from adaptive_decision.slow_attack_detector import detect_slow_attack
from adaptive_decision.monitoring_logger import log_event

user_id = "user123"

for i in range(8):

    risk_score = random.uniform(0, 1)

    decision = adaptive_decision(risk_score)

    slow_attack = detect_slow_attack(user_id)

    event = {
        "attempt": i+1,
        "user_id": user_id,
        "risk_score": round(risk_score, 2),
        "decision": decision,
        "slow_attack_detected": slow_attack
    }

    log_event(event)

    print("Attempt:", i+1)
    print("Risk Score:", round(risk_score, 2))
    print("Decision:", decision)
    print("Slow Attack:", slow_attack)
    print("-" * 30)