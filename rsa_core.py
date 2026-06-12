"""
RSA logic
  1. Select primes p and q
  2. Calculate n = p * q
  3. Calculate phi(n) = (p - 1)(q - 1)
  4. Select e with 1 < e < phi and gcd(e, phi) = 1
  5. Determine d: d*e mod phi = 1 and d < phi
  6. Publish public key  PU = {e, n}
  7. Keep secret private key PR = {d, n}
"""
import math
# KEY DERIVATION

def is_prime(x):
    """Trial-division primality test (slide step 1 requires p, q prime)."""
    if x < 2:
        return False
    return all(x % k for k in range(2, int(math.isqrt(x)) + 1))


def factor_n(n):
    """
    Recover the primes p and q from n by trial division.
    """
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            p, q = i, n // i
            if not (is_prime(p) and is_prime(q)):
                raise ValueError(f"n={n} is not a product of two primes")
            return p, q
    raise ValueError(f"Could not factor n={n}")


def mod_inverse(e, phi):
    """
    determine d such that d*e mod phi = 1 and d < phi.
    """
    if math.gcd(e, phi) != 1:
        raise ValueError("gcd(e, phi) != 1 — invalid key pair")
    return pow(e, -1, phi)


def derive_private_key(n, e):
    """
    derive private key : d
    """
    p, q = factor_n(n)
    assert p * q == n
    phi = (p - 1) * (q - 1)
    if not (1 < e < phi):
        raise ValueError(f"e={e} must be between 1 and phi={phi}")
    d = mod_inverse(e, phi)
    return d


# ENCRYPTION / DECRYPTION 

def encrypt_block(m, e, n):
    if not (0 <= m < n):
        raise ValueError(f"Block value {m} out of range [0, n)")
    return pow(m, e, n)


def decrypt_block(c, d, n):
    return pow(c, d, n)