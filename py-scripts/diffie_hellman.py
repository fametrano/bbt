from hashlib import sha256 as hf

from btclib import dsa
from btclib.ecc.curve import mult
from btclib.ecc.curve import secp256k1 as ec
from btclib.dh import ansi_x9_63_kdf

# Diffie-Hellman
print("\n Diffie-Hellman")

a, A = dsa.gen_keys()  # Alice
b, B = dsa.gen_keys()  # Bob

# Alice calculates the shared secret using Bob's public key
shared_secret_a = mult(a, B)

# Bob calculates the shared secret using Alice's public key
shared_secret_b = mult(b, A)

print("same shared secret:", shared_secret_a == shared_secret_b)
print("as expected:", shared_secret_a == mult(a * b, ec.G))

# hash the shared secret to remove weak bits
shared_secret_field_element = shared_secret_a[0]
z = shared_secret_field_element.to_bytes(ec.psize, "big")
shared_info = None
shared_key = ansi_x9_63_kdf(z, 32, hf, shared_info)
print("shared key:", shared_key.hex())
