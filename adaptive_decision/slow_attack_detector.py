from collections import defaultdict

attempts = defaultdict(int)

def detect_slow_attack(user_id):
    
    attempts[user_id] += 1

    if attempts[user_id] > 5:
        return True

    return False