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

from btclib.curve import secp256k1 as ec
from btclib.curvegroup import _double_mult, _mult

random.seed(42)

# setup
us = []
vs = []
QJs = []
for _ in range(500):
    us.append(random.getrandbits(ec.nlen) % ec.n)
    vs.append(random.getrandbits(ec.nlen) % ec.n)
    q = random.getrandbits(ec.nlen) % ec.n
    QJs.append(_mult(q, ec.GJ, ec))

"""
for u, v, QJ in zip(us, vs, QJs):
    t1 = ec._add_jac(_mult(u, ec.GJ, ec), _mult(v, QJ, ec))
    t2 = _double_mult(u, ec.GJ, v, QJ, ec)
    assert ec._jac_equality(t1, t2)
"""

start = time.time()
for u, v, QJ in zip(us, vs, QJs):
    ec._add_jac(_mult(u, ec.GJ, ec), _mult(v, QJ, ec))
elapsed1 = time.time() - start

start = time.time()
for u, v, QJ in zip(us, vs, QJs):
    _double_mult(u, ec.GJ, v, QJ, ec)
elapsed2 = time.time() - start

print(f"{elapsed2 / elapsed1:.0%}")
