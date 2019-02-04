#!/usr/bin/env python3

# Copyright (C) 2017-2019 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import random
import time
from hashlib import sha256

from btclib.curve import mult
from btclib.curves import secp256k1
from btclib.ssa import sign, verify, batch_verify

random.seed(42)

ec = secp256k1
hf = sha256
hsize = hf().digest_size
hlen = hsize * 8

# n = 1 loops forever and does not really test batch verify
n_sig = [2, 4, 8, 16, 32, 64, 128]
m = []
sig = []
Q = []
for j in range(max(n_sig)):
    m.append(random.getrandbits(hlen).to_bytes(hsize, 'big'))
    q = random.getrandbits(ec.nlen) % ec.n
    sig.append(sign(ec, hf, m[j], q))
    Q.append(mult(ec, q, ec.G))

for n in n_sig:

    # no batch
    start = time.time()
    for j in range(n):
        assert verify(ec, hf, m[j], Q[j], sig[j])
    elapsed1 = time.time() - start

    # batch
    start = time.time()
    assert batch_verify(ec, hf, m[:n], Q[:n], sig[:n])
    elapsed2 = time.time() - start

    print(n, elapsed2 / elapsed1)
