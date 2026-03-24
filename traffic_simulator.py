import random
import time
from datetime import datetime
from auth.user_manager import User
from attacks.attack_simulator import AttackSimulator, load_rockyou
import csv

# ----------------------------
# Configuration
# ----------------------------

TOTAL_EVENTS = 300
LEGITIMATE_PROB = 0.5   # balanced dataset

# ----------------------------
# Setup
# ----------------------------

print("Creating users...")

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

print("Loading RockYou subset...")
wordlist = load_rockyou("rockyou.txt", limit=10000)
print("Loaded", len(wordlist), "passwords.\n")

simulator = AttackSimulator(users, wordlist)

all_events = []

print("\n--- Simulating Mixed Login Traffic ---\n")

# ----------------------------
# Simulation
# ----------------------------

for i in range(TOTAL_EVENTS):

    r = random.random()

    # ----------------------------
    # Legitimate
    # ----------------------------
    if r < LEGITIMATE_PROB:

        simulator.run_legitimate(count=1)
        print(f"[{i+1}] Legitimate Login")

        time.sleep(random.uniform(0.5, 2))  # natural delay


    # ----------------------------
    # Attack Traffic
    # ----------------------------
    else:

        attack_type = random.choice(["dictionary", "rapid", "slow", "replay"])

        # ----------------------------
        # Dictionary Attack
        # ----------------------------
        if attack_type == "dictionary":

            simulator.run_dictionary_attack(count=1)
            print(f"[{i+1}] Dictionary Attack")

            time.sleep(random.uniform(0.2, 1))


        # ----------------------------
        # Rapid Burst Attack
        # ----------------------------
        elif attack_type == "rapid":

            print(f"[{i+1}] Rapid Burst Attack")

            # VERY fast attempts
            for _ in range(10):
                simulator.run_dictionary_attack(count=1)
                time.sleep(0.05)   # key signal


        # ----------------------------
        # Low-and-Slow Attack
        # ----------------------------
        elif attack_type == "slow":

            print(f"[{i+1}] Low-and-Slow Attack")

            for _ in range(5):
                simulator.run_dictionary_attack(count=1)
                time.sleep(2.5)   # key signal


        # ----------------------------
        # Replay Attack
        # ----------------------------
        elif attack_type == "replay":

            simulator.run_replay_attack()
            print(f"[{i+1}] Replay Attack")

            time.sleep(0.5)


# ----------------------------
# Collect Events
# ----------------------------

all_events = simulator.get_events()

print("\n--- Simulation Complete ---")
print("Total Events Generated:", len(all_events))


# ----------------------------
# Add Time Gap Feature (IMPORTANT)
# ----------------------------

previous_time = None

for event in all_events:

    current_time = datetime.fromtimestamp(int(event["timestamp"]))

    if previous_time is None:
        event["time_gap"] = 0
    else:
        event["time_gap"] = (current_time - previous_time).total_seconds()

    previous_time = current_time
# ----------------------------
# Write CSV
# ----------------------------

csv_file = "login_events.csv"

with open(csv_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=all_events[0].keys())
    writer.writeheader()
    writer.writerows(all_events)

print("Events saved to", csv_file)