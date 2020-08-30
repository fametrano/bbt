#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

""" Deterministic Key Sequence (Type-1)"""

import secrets
from hashlib import sha256 as hf

from btclib.curvemult import mult
from btclib.curves import secp256k1 as ec
from btclib.utils import int_from_bits

# master prvkey in [1, n-1]
mprvkey = 1 + secrets.randbelow(ec.n - 1)
print(f"\nmaster prvkey: {hex(mprvkey).upper()}")

# Master Pubkey:
mpubkey = mult(mprvkey, ec.G)
print(f"Master Pubkey: {hex(mpubkey[0]).upper()}")
print(f"               {hex(mpubkey[1]).upper()}")

r = secrets.randbits(ec.nlen)
print(f"\npublic random number: {hex(r).upper()}")

rbytes = r.to_bytes(ec.nsize, "big")
nKeys = 3
for i in range(nKeys):
    ibytes = i.to_bytes(ec.nsize, "big")
    hd = hf(ibytes + rbytes).digest()
    offset = int_from_bits(hd, ec.nlen) % ec.n
    q = (mprvkey + offset) % ec.n
    Q = mult(q, ec.G, ec)
    print(f"\nprvkey #{i}: {hex(q).upper()}")
    print(f"Pubkey #{i}: {hex(Q[0]).upper()}")
    print(f"           {hex(Q[1]).upper()}")

# Pubkeys could also be calculated without using prvkeys
for i in range(nKeys):
    ibytes = i.to_bytes(ec.nsize, "big")
    hd = hf(ibytes + rbytes).digest()
    offset = int_from_bits(hd, ec.nlen) % ec.n
    Q = ec.add(mpubkey, mult(offset, ec.G, ec))
    assert Q == mult((mprvkey + offset) % ec.n, ec.G, ec)
