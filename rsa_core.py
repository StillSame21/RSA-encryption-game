""" Function for encrytion and decryption """

import math

def factor_n(n):
    for i in range(2, int(math.isqrt(n))+1):
        if n% i == 0:
            return i, n // i
    raise ValueError(f"Could not factor n={n}")

def mod_inverse(e, phi):
    if math.gcd(e, phi) != 1:
        raise ValueError("gcd(e,phi) != 1 - invalid key pair")
    return pow(e,-1,phi)

def derive_private_key(n,e):
    p, q = factor_n(n)
    phi = (p-1)*(q-1)
    d = mod_inverse(e,phi)
    return d

# 2. CORE ENCRYPTION / DECRYPTION 

def ecrypt_block(m,e,n):
    if not (0 <= m < n):
        raise ValueError(f"Block value {m} out of range [0, n]")
    return pow(m,e,n)

def decrypt_block(c,d,n):
    return pow(c,d,n)
