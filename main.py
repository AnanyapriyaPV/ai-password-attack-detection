import random
import time
from auth.user_manager import User
from attacks.attack_simulator import AttackSimulator, load_rockyou
import csv

# ----------------------------
# Configuration
# ----------------------------

TOTAL_EVENTS = 30
LEGITIMATE_PROB = 0.6  # 60% normal traffic

# ----------------------------
# Setup
# ----------------------------

print("Creating user...")
user = User("alice", "admin123")

print("Loading RockYou subset...")
wordlist = load_rockyou("rockyou.txt", limit=10000)
print("Loaded", len(wordlist), "passwords.\n")

all_events = []

simulator = AttackSimulator(user, wordlist)

print("\n--- Simulating Mixed Login Traffic ---\n")

# ----------------------------
# Traffic Simulation
# ----------------------------

for i in range(TOTAL_EVENTS):

    event_type_selector = random.random()

    # ---- Legitimate Traffic ----
    if event_type_selector < LEGITIMATE_PROB:
        simulator.run_legitimate(count=1)
        print(f"[{i+1}] Legitimate Login")

    # ---- Attack Traffic ----
    else:
        attack_choice = random.choice(
            ["dictionary", "rapid", "slow", "replay"]
        )

        if attack_choice == "dictionary":
            simulator.run_dictionary_attack(count=1)
            print(f"[{i+1}] Dictionary Attack")
        
        elif attack_choice == "rapid":
            simulator.run_rapid_burst(count=15)
            print(f"[{i+1}] Rapid Burst Attack (15 attempts)")

        elif attack_choice == "slow":
            simulator.run_low_and_slow(count=5)
            print(f"[{i+1}] Low-and-Slow Attack (5 attempts spaced out)")

        elif attack_choice == "replay":
            simulator.run_replay_attack()
            print(f"[{i+1}] Replay Attack")

    time.sleep(random.uniform(0.1, 1.5))

# After loop
all_events = simulator.get_events()

print("\n--- Simulation Complete ---\n")
print("Total Events Generated:", len(all_events))

# ----------------------------
# Write to CSV
# ----------------------------

csv_file = "login_events.csv"

with open(csv_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=all_events[0].keys())
    writer.writeheader()
    writer.writerows(all_events)

print("Events saved to", csv_file)