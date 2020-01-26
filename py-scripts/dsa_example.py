#!/usr/bin/env python3

# Copyright (C) 2017-2019 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from hashlib import sha256 as hf

from btclib.curvemult import mult
from btclib.curves import secp256k1 as ec
from btclib.dsa import sign
from btclib.numbertheory import mod_inv

print("\n*** EC:")
print(ec)

q = 0x18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725
q = q % ec.n
print("\n*** Key Generation:")
print("prvkey:   ", hex(q))

Q = mult(q, ec.G)
print("PubKey:", "02" if (Q[1] % 2 == 0) else "03", hex(Q[0]))

print("\n*** Message to be signed")
msg = "Paolo is afraid of ephemeral random numbers"
print(msg)

print("*** Hash digest of the message")
msghd = hf(msg.encode()).digest()
# hash(msg) must be transformed into an integer modulo ec.n:
c = int.from_bytes(msghd, 'big') % ec.n
assert c != 0
print("    c:", hex(c))

print("\n*** Sign Message")
# ephemeral key k must be kept secret and never reused !!!!!
# good choice: k = hf(q||c)
# different for each msg, private because of q
temp = q.to_bytes(32, 'big') + c.to_bytes(32, 'big')
k_bytes = hf(temp).digest()
k = int.from_bytes(k_bytes, 'big') % ec.n
assert 0 < k < ec.n, "Invalid ephemeral key"
print("eph k:", hex(k))

K = mult(k, ec.G)

r = K[0] % ec.n
# if r == 0 (extremely unlikely for large ec.n) go back to a different k
assert r != 0

s = (c + r*q) * mod_inv(k, ec.n) % ec.n
# if s == 0 (extremely unlikely for large ec.n) go back to a different k
assert s != 0

print("    r:", hex(r))
print("    s:", hex(s))

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
print("    r:", hex(r))
print("   sm:", hex(sm))

print("*** Malleated Signature Verification")
w = mod_inv(sm, ec.n)
u = c*w %ec.n
v = r*w %ec.n
assert u != 0
assert v != 0
U = mult(u, ec.G)
V = mult(v, Q)
x, y = ec.add(U, V)
print(r == x %ec.n)

print("\n*** Another message")
msg2 = "and Paolo is right to be afraid"
print(msg2)

print("*** Hash digest of the message")
msghd2 = hf(msg2.encode()).digest()
# hash(msg) must be transformed into an integer modulo ec.n:
c2 = int.from_bytes(msghd, 'big') % ec.n
assert c2 != 0
print("    c2:", hex(c2))

print("\n*** Signature")
#very bad! Never reuse an ephemeral key!!!
k2 = k
print("eph k2:", hex(k2))

K2 = mult(k2, ec.G)

r = K2[0] % ec.n
# if r == 0 (extremely unlikely for large ec.n) go back to a different k
assert r != 0

s2 = (c2 + r*q) * mod_inv(k2, ec.n) %ec.n
# if s2 == 0 (extremely unlikely for large ec.n) go back to a different k
assert s2 != 0

print("     r:", hex(r))
print("    s2:", hex(s2))

print("*** Signature Verification")
w = mod_inv(s2, ec.n)
u = c2*w %ec.n
v = r*w %ec.n
assert u != 0
assert v != 0
U = mult(u, ec.G)
V = mult(v, Q)
x, y = ec.add(U, V)
print(r == x % ec.n)
