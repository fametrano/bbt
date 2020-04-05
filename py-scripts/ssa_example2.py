#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from hashlib import sha256

from btclib.curvemult import mult, double_mult
from btclib.curves import secp256k1 as ec
from btclib.numbertheory import mod_inv
from btclib.utils import int_from_bits
from btclib.ssa import _challenge

print("\n*** EC:")
print(ec)

print("\n*** Key Generation:")
q = 0x18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725
q = q % ec.n
Q = mult(q, ec.G)
if not ec.has_square_y(Q):
    q = ec.n - q
    Q = (Q[0], ec._p - Q[1])
print(f"prvkey: {hex(q).upper()}")
print(f"PubKey: {hex(Q[0]).upper()}")


print("\n*** Message to be signed")
orig_msg1 = "Paolo is afraid of ephemeral random numbers"
msg1 = sha256(orig_msg1.encode()).digest()
print(msg1.hex().upper())


print("\n*** Ephemeral key and Challenge")
# ephemeral key k must be kept secret and never reused !!!!!
# good choice: k = hf(q||msg)
# different for each msg, private because of q
temp = q.to_bytes(32, 'big') + msg1
k1_bytes = sha256(temp).digest()
k1 = int.from_bytes(k1_bytes, 'big') % ec.n
k1 = int_from_bits(k1_bytes, ec.nlen) % ec.n
assert 0 < k1 < ec.n, "Invalid ephemeral key"
print(f"eph k: {hex(k1).upper()}")

K1 = mult(k1, ec.G)
c1 = _challenge(K1[0], Q[0], msg1, ec, sha256)
print(f"   c1: {hex(c1).upper()}")


print("\n*** Sign Message")
r1 = K1[0]
s1 = (k1 + c1*q) % ec.n
print(f"   r1: {hex(r1).upper()}")
print(f"   s1: {hex(s1).upper()}")


print("*** Verify Signature")
K = double_mult(-c1, Q, s1, ec.G)
print(K[0] == r1)


print("\n*** Another message to sign")
orig_msg2 = "and Paolo is right to be afraid"
msg2 = sha256(orig_msg2.encode()).digest()
print(msg2.hex().upper())


print("\n*** Ephemeral key and Challenge")
# ephemeral key k must be kept secret and never reused !!!!!
k2 = k1
print(f"eph k: {hex(k2).upper()}")

K2 = mult(k2, ec.G)
c2 = _challenge(K2[0], Q[0], msg2, ec, sha256)
print(f"   c2: {hex(c2).upper()}")


print("\n*** Sign Message")
r2 = K2[0]
s2 = (k2 + c2*q) % ec.n
print(f"   r2: {hex(r2).upper()}")
print(f"   s2: {hex(s2).upper()}")


print("*** Verify Signature")
K = double_mult(-c2, Q, s2, ec.G)
print(K[0] == r2)
