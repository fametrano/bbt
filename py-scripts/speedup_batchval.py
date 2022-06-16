#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import random
import time
from hashlib import sha256 as hf

from btclib.ecc.curve import mult
from btclib.ecc.curve import secp256k1 as ec
from btclib.ecc.ssa import _batch_verify, _sign, _verify

random.seed(42)

hsize = hf().digest_size
hlen = hsize * 8

# n = 1 loops forever and does not really test batch verify
n_sig = [4, 8, 16, 32, 64, 128, 256, 512]
m = [random.getrandbits(hlen).to_bytes(hsize, "big") for _ in range(max(n_sig))]
q = [random.getrandbits(ec.nlen) % ec.n for _ in m]
sig = [_sign(msg, qq) for msg, qq in zip(m, q)]
Q = [mult(qq, ec.G)[0] for qq in q]

for n in n_sig:

    # no batch
    start = time.time()
    for j in range(n):
        assert _verify(m[j], Q[j], sig[j])
    elapsed1 = time.time() - start

    # batch
    ms = m[:n]
    Qs = Q[:n]
    sigs = sig[:n]
    start = time.time()
    assert _batch_verify(ms, Qs, sigs), n
    elapsed2 = time.time() - start

    print(n, elapsed2 / elapsed1)
