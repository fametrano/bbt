#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

""" Deterministic Wallet (Type-2)"""

import secrets
from hashlib import sha256 as hf

from btclib.curvemult import mult
from btclib.curves import secp256k1 as ec
from btclib.utils import int_from_bits

# master prvkey
mprvkey = 1 + secrets.randbelow(ec.n-1)
print(f'\nmaster prv key = {hex(mprvkey).upper()}')

# Master Pubkey:
mpubkey = mult(mprvkey, ec.G)
print(f'Master Pub Key: {hex(mpubkey[0]).upper()}')
print(f'                {hex(mpubkey[1]).upper()}')

# public random number
r = secrets.randbits(ec.nlen)
print('\npublic random number:', format(r, '#064x'))

rbytes = r.to_bytes(ec.nsize, 'big')
nKeys = 3
for i in range(nKeys):
    ibytes = i.to_bytes(ec.nsize, 'big')
    hd = hf(ibytes + rbytes).digest()
    offset = int_from_bits(hd, ec.nlen) % ec.n
    q = (mprvkey + offset) % ec.n
    Q = mult(q, ec.G)
    print(f'\nprvkey# {i}: {hex(q).upper()}')
    print(f'Pubkey# {i}: {hex(Q[0]).upper()}')
    print(f'           {hex(Q[1]).upper()}')

# Pubkeys could be calculated without using prvkeys
for i in range(nKeys):
    ibytes = i.to_bytes(ec.nsize, 'big')
    hd = hf(ibytes + rbytes).digest()
    offset = int_from_bits(hd, ec.nlen) % ec.n
    Q = ec.add(mpubkey, mult(offset))
    assert Q == mult((mprvkey + offset) % ec.n)
