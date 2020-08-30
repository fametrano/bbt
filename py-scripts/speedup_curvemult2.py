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

from btclib.curvemult import _mult_jac
from btclib.curvemult2 import (
    _mult_base_3,
    _mult_fixed_window,
    _mult_mont_ladder,
    _mult_sliding_window,
    _mult_w_NAF,
)
from btclib.curves import secp256k1 as ec

# setup
random.seed(42)
qs = [random.getrandbits(ec.nlen) % ec.n for _ in range(100)]

start = time.time()
for q in qs:
    _mult_jac(q, ec.GJ, ec)
benchmark_time = time.time() - start

start = time.time()
for q in qs:
    _mult_mont_ladder(q, ec.GJ, ec)
elapsed = time.time() - start
print(f"Montgomery ladder: {elapsed / benchmark_time:.0%}")

start = time.time()
for q in qs:
    _mult_base_3(q, ec.GJ, ec)
elapsed = time.time() - start
print(f"Base 3           : {elapsed / benchmark_time:.0%}")

start = time.time()
w = 4
for q in qs:
    _mult_fixed_window(q, ec.GJ, w, ec)
elapsed = time.time() - start
print(f"Fixed window {w}   : {elapsed / benchmark_time:.0%}")

start = time.time()
w = 5
for q in qs:
    _mult_fixed_window(q, ec.GJ, w, ec)
elapsed = time.time() - start
print(f"Fixed window {w}   : {elapsed / benchmark_time:.0%}")

start = time.time()
for q in qs:
    _mult_sliding_window(q, ec.GJ, 5, ec)
elapsed = time.time() - start
print(f"Sliding window   : {elapsed / benchmark_time:.0%}")

start = time.time()
for q in qs:
    _mult_w_NAF(q, ec.GJ, 4, ec)
elapsed = time.time() - start
print(f"wNAF             : {elapsed / benchmark_time:.0%}")
