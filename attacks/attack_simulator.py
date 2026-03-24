from itertools import count
import time
import random
from auth.session_auth import authenticate_login
from auth.vulnerability import calculate_entropy

# ---------------------------
# Load RockYou Safely
# ---------------------------

def load_rockyou(filepath, limit=10000):
    passwords = []
    with open(filepath, "r", encoding="latin-1") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            pwd = line.strip()
            if pwd:
                passwords.append(pwd)
    return passwords

# ---------------------------
# Standardized Event Builder
# ---------------------------

def build_event(user, auth_result, attack_type, password_attempt, wordlist):

    label = 0 if attack_type == "legitimate" else 1

    dictionary_flag = 1 if password_attempt in wordlist else 0

    return {
        "timestamp": auth_result["timestamp"],
        "user_id": user.user_id,
        "password_attempt": password_attempt,   # NEW
        "dictionary_flag": dictionary_flag,     # NEW
        "hmac_valid": auth_result["hmac_valid"],
        "password_valid": auth_result["password_valid"],
        "failed_attempts": auth_result["failed_attempts"],
        "vulnerability_score": auth_result["vulnerability_score"],
        "attack_type": attack_type,
        "password_entropy": calculate_entropy(password_attempt),
        "label": label
    }

# ---------------------------
# Attack Simulator Class
# ---------------------------

class AttackSimulator:

    def __init__(self, users, wordlist):
        self.users = users
        self.wordlist = wordlist
        self.events = []

    # ---------------------------
    # Legitimate Login
    # ---------------------------

    def get_random_user(self):
        return random.choice(self.users)

    def run_legitimate(self, count=3):
        for _ in range(count):
            user = self.get_random_user()
            password = user.password
            result = authenticate_login(user, password)

            event = build_event(user, result, "legitimate", password, self.wordlist)

            self.events.append(event)
            time.sleep(1)

    # ---------------------------
    # Dictionary Attack
    # ---------------------------

    def run_dictionary_attack(self, count=5):
        for _ in range(count):
            user = self.get_random_user()
            password_guess = random.choice(self.wordlist)

            result = authenticate_login(user, password_guess)

            event = build_event(user, result, "dictionary", password_guess, self.wordlist)

            self.events.append(event)

    # ---------------------------
    # Rapid Burst Attack
    # ---------------------------

    def run_rapid_burst(self, count=5):
        for _ in range(count):
            user = self.get_random_user()
            password_guess = random.choice(self.wordlist)

            result = authenticate_login(user, password_guess)
            event = build_event(user, result, "rapid_burst", password_guess, self.wordlist)

            self.events.append(event)
            # No sleep → rapid burst

    # ---------------------------
    # Low-and-Slow Attack
    # ---------------------------

    def run_low_and_slow(self, count=5):
        for _ in range(count):
            user = self.get_random_user()
            password_guess = random.choice(self.wordlist)

            result = authenticate_login(user, password_guess)
            event = build_event(user, result, "low_and_slow", password_guess, self.wordlist)

            self.events.append(event)
            time.sleep(3)

    # ---------------------------
    # Replay Attack
    # ---------------------------

    def run_replay_attack(self):
        user = self.get_random_user()
        password = user.password
        # First legitimate attempt
        result1 = authenticate_login(user, password)
        event1 = build_event(user, result1, "legitimate", password, self.wordlist)
        self.events.append(event1)

        # Replay attempt
        result2 = authenticate_login(user, password)
        event2 = build_event(user, result2, "replay", password, self.wordlist)
        self.events.append(event2)

    def get_events(self):
        return self.events