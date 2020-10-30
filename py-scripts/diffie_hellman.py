from btclib import dsa
from btclib.curvemult import mult
from btclib.curves import secp256k1 as ec
from btclib.dh import ansi_x963_kdf
from hashlib import sha256 as hf

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
shared_key = ansi_x963_kdf(z, 32, ec, hf)  # hashed using the key generation function
print("shared key:", shared_key.hex())
