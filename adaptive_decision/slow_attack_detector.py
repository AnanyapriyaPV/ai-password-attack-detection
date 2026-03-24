from collections import defaultdict
import time

attempts = defaultdict(list)

def detect_slow_attack(user_id):

    now = time.time()
    attempts[user_id].append(now)

    # Keep last 10 timestamps
    attempts[user_id] = attempts[user_id][-10:]

    if len(attempts[user_id]) < 5:
        return False

    # Check if attempts spread out (slow attack)
    time_diff = attempts[user_id][-1] - attempts[user_id][0]

    return time_diff > 5   # slow spread