import random
from auth.math_utils import modular_exponentiation

# Public parameters (small for simulation)
p = 23   # prime
g = 5    # generator

def generate_private_key():
    return random.randint(2, p - 2)

def generate_public_key(private_key):
    return modular_exponentiation(g, private_key, p)

def generate_shared_key(their_public, my_private):
    return modular_exponentiation(their_public, my_private, p)