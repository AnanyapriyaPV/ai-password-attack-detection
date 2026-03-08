import hmac
import hashlib
import time
import secrets

NONCE_STORE = set()

def generate_nonce():
    return secrets.token_hex(16)

def create_hmac(shared_key: int, password: str, nonce: str, timestamp: str):
    key_bytes = str(shared_key).encode()
    message = (password + nonce + timestamp).encode()
    return hmac.new(key_bytes, message, hashlib.sha512).hexdigest()

def verify_hmac(shared_key, password, nonce, timestamp, received_hmac):
    # Replay protection
    if nonce in NONCE_STORE:
        return False
    
    expected = create_hmac(shared_key, password, nonce, timestamp)
    
    if hmac.compare_digest(expected, received_hmac):
        NONCE_STORE.add(nonce)
        return True
    
    return False