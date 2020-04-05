#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from hashlib import sha256

from btclib.curvemult import mult
from btclib.curves import secp256k1 as ec
from btclib.numbertheory import mod_inv
from btclib.utils import int_from_bits

print("\n*** EC:")
print(ec)

print("\n*** Key Generation:")
q = 0x18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725
q = q % ec.n
print("prvkey:   ", hex(q))
Q = mult(q, ec.G)
print("PubKey:", "02" if (Q[1] % 2 == 0) else "03", hex(Q[0]))


print("\n*** Message to be signed")
msg = "Paolo is afraid of ephemeral random numbers"
print(msg)


print("\n*** Challenge and Ephemeral key")
msghd = sha256(msg.encode()).digest()
# hash(msg) must be transformed into an integer modulo ec.n:
c = int.from_bytes(msghd, 'big') % ec.n
c = int_from_bits(msghd, ec.nlen) % ec.n
assert c != 0
print(f"    c: {hex(c).upper()}")

# ephemeral key k must be kept secret and never reused !!!!!
# good choice: k = hf(q||c)
# different for each msg, private because of q
temp = q.to_bytes(32, 'big') + c.to_bytes(32, 'big')
k_bytes = sha256(temp).digest()
k = int.from_bytes(k_bytes, 'big') % ec.n
k = int_from_bits(k_bytes, ec.nlen) % ec.n
assert 0 < k < ec.n, "Invalid ephemeral key"
print(f"eph k: {hex(k).upper()}")


print("\n*** Sign Message")
K = mult(k, ec.G)
r = K[0] % ec.n
# if r == 0 (extremely unlikely for large ec.n) go back to a different k
assert r != 0
s = (c + r*q) * mod_inv(k, ec.n) % ec.n
# if s == 0 (extremely unlikely for large ec.n) go back to a different k
assert s != 0
print(f"   r: {hex(r).upper()}")
print(f"   s: {hex(s).upper()}")


print("*** Verify Signature")
w = mod_inv(s, ec.n)
u = (c*w) %ec.n
v = (r*w) %ec.n
assert u != 0
assert v != 0
U = mult(u, ec.G)
V = mult(v, Q)
x, y = ec.add(U, V)
print(r == x %ec.n)


print("\n*** Malleated Signature")
sm = ec.n - s
print(f"   r: {hex(r).upper()}")
print(f"  sm: {hex(sm).upper()}")


print("*** Verify Malleated Signature")
w = mod_inv(sm, ec.n)
u = c*w %ec.n
v = r*w %ec.n
assert u != 0
assert v != 0
U = mult(u, ec.G)
V = mult(v, Q)
x, y = ec.add(U, V)
print(r == x %ec.n)


print("\n*** Another message to sign")
msg2 = "and Paolo is right to be afraid"
print(msg2)


print("\n*** Challenge and Ephemeral key")
msghd2 = sha256(msg2.encode()).digest()
# hash(msg) must be transformed into an integer modulo ec.n:
c2 = int.from_bytes(msghd, 'big') % ec.n
c2 = int_from_bits(msghd, ec.nlen) % ec.n
assert c2 != 0
print(f"    c2: {hex(c2).upper()}")

#very bad! Never reuse an ephemeral key!!!
k2 = k
print(f"eph k2: {hex(k2).upper()}")


print("\n*** Sign Message")
K2 = mult(k2, ec.G)
r = K2[0] % ec.n
# if r == 0 (extremely unlikely for large ec.n) go back to a different k
assert r != 0
s2 = (c2 + r*q) * mod_inv(k2, ec.n) %ec.n
# if s2 == 0 (extremely unlikely for large ec.n) go back to a different k
assert s2 != 0
print(f"    r: {hex(r).upper()}")
print(f"   s2: {hex(s2).upper()}")


print("*** Verify Signature")
w = mod_inv(s2, ec.n)
u = c2*w %ec.n
v = r*w %ec.n
assert u != 0
assert v != 0
U = mult(u, ec.G)
V = mult(v, Q)
x, y = ec.add(U, V)
print(r == x % ec.n)
