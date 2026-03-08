import time
from auth.diffie_hellman import *
from auth.hmac_auth import *
from auth.hashing import verify_password

def authenticate_login(user, password_attempt):
    # ---- Fresh DH per login ----
    a = generate_private_key()
    A = generate_public_key(a)

    b = generate_private_key()
    B = generate_public_key(b)

    shared_client = generate_shared_key(B, a)
    shared_server = generate_shared_key(A, b)

    # ---- Nonce + Timestamp ----
    nonce = generate_nonce()
    timestamp = str(int(time.time()))

    # ---- Create HMAC ----
    hmac_value = create_hmac(shared_client, password_attempt, nonce, timestamp)

    # ---- Verify HMAC ----
    hmac_valid = verify_hmac(
        shared_server,
        password_attempt,
        nonce,
        timestamp,
        hmac_value
    )

    # ---- Verify Password Hash ----
    password_valid = verify_password(password_attempt, user.password_hash)

    # Update user failed attempts
    if password_valid:
        user.failed_attempts = 0
    else:
        user.failed_attempts += 1

    user.update_vulnerability()

    return {
        "user_id": user.user_id,
        "timestamp": timestamp,
        "password_attempt": password_attempt,
        "hmac_valid": hmac_valid,
        "password_valid": password_valid,
        "failed_attempts": user.failed_attempts,
        "vulnerability_score": user.vulnerability_score
    }