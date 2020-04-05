#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from btclib.curvemult import mult
from btclib.curves import secp256k1 as ec
from btclib.dsa import recover_pubkeys, sign, verify

print("\n*** EC:")
print(ec)

q = 0x18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725
q = q % ec.n
print("\n*** Key Generation:")
print(f"prvkey:    {hex(q).upper()}")

Q = mult(q, ec.G)
print(f"PubKey: {'02' if Q[1] % 2 == 0 else '03'} {hex(Q[0]).upper()}")

print("\n*** Message to be signed")
msg1 = "Paolo is afraid of ephemeral random numbers"
print(msg1)

print("\n*** Sign Message")
r1, s1 = sign(msg1, q)
print(f"   r1: {hex(r1).upper()}")
print(f"   s1: {hex(s1).upper()}")

print("*** Verify Signature")
print(verify(msg1, Q, (r1, s1)))

print("\n*** Recover keys")
keys = recover_pubkeys(msg1, (r1, s1))
for key in keys:
    print(f"{'02' if key[1] % 2 == 0 else '03'} {hex(key[0]).upper()}")

print("\n*** Malleated Signature")
sm = ec.n - s1
print(f"   r1: {hex(r1).upper()}")
print(f"   sm: {hex(sm).upper()}")

print("\n*** Recover keys")
keys = recover_pubkeys(msg1, (r1, sm))
for key in keys:
    print(f"{'02' if key[1] % 2 == 0 else '03'} {hex(key[0]).upper()}")

print("*** Verify Malleated Signature")
print(verify(msg1, Q, (r1, sm)))

print("\n*** Another message to sign")
msg2 = "and Paolo is right to be afraid"
print(msg2)

print("\n*** Sign Message")
r2, s2 = sign(msg2, q)
print(f"   r2: {hex(r2).upper()}")
print(f"   s2: {hex(s2).upper()}")

print("*** Verify Signature")
print(verify(msg2, Q, (r2, s2)))

print("\n*** Recover keys")
keys = recover_pubkeys(msg2, (r2, s2))
for key in keys:
    print(f"{'02' if key[1] % 2 == 0 else '03'} {hex(key[0]).upper()}")
