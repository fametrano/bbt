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

from btclib.curve import mult
from btclib.curve import secp256k1 as ec
from btclib.utils import int_from_bits

# master prvkey
mprvkey = 1 + secrets.randbelow(ec.n - 1)
print(f"\nmaster private key = {hex(mprvkey).upper()}")

mprvkey_bytes = mprvkey.to_bytes(ec.nlen, "big")
nKeys = 3
for i in range(nKeys):
    ibytes = i.to_bytes(ec.nlen, "big")
    hd = hf(ibytes + mprvkey_bytes).digest()
    q = int_from_bits(hd, ec.nlen) % ec.n
    Q = mult(q, ec.G)
    print(f"\nprvkey# {i}: {hex(q).upper()}")
    print(f"Pubkey# {i}: {hex(Q[0]).upper()}")
    print(f"           {hex(Q[1]).upper()}")
