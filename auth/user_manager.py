from auth.hashing import hash_password, verify_password
from auth.vulnerability import calculate_vulnerability

class User:
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.password_hash = hash_password(password)
        self.failed_attempts = 0
        self.account_locked = False
        self.vulnerability_score = calculate_vulnerability(password, 0)

    def authenticate(self, password_attempt):
        if verify_password(password_attempt, self.password_hash):
            self.failed_attempts = 0
            return True
        else:
            self.failed_attempts += 1
            self.update_vulnerability()
            return False

    def update_vulnerability(self):
        fail_ratio = min(self.failed_attempts / 10, 1)
        self.vulnerability_score = calculate_vulnerability(
            self.password, fail_ratio
        )