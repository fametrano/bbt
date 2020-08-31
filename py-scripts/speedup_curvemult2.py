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

from btclib.curvegroup import (
    _mult_base_3,
    _mult_fixed_window,
    _mult_jac,
    _mult_mont_ladder,
)
from btclib.curvemult2 import _mult_sliding_window, _mult_w_NAF
from btclib.curves import secp256k1 as ec

# setup
random.seed(42)
qs = [random.getrandbits(ec.nlen) % ec.n for _ in range(300)]

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_jac(q, T, ec)
double_and_add = time.time() - start
print("double_and_add completed")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_mont_ladder(q, T, ec)
montgomery = time.time() - start
print("montgomery completed")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_base_3(q, T, ec)
base3 = time.time() - start
print("base3 completed")

T = ec.GJ
start = time.time()
w = 4
for q in qs:
    T = _mult_fixed_window(q, T, ec, w)
fixed_window_4 = time.time() - start
print("fixed_window_4 completed")

T = ec.GJ
start = time.time()
w = 5
for q in qs:
    T = _mult_fixed_window(q, T, ec, w)
fixed_window_5 = time.time() - start
print("fixed_window_5 completed")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_sliding_window(q, T, ec, 5)
sliding_window = time.time() - start
print("sliding_window completed")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_w_NAF(q, T, ec, 4)
wNAF = time.time() - start
print("wNAF completed")

print("-----")
benchmark_time = fixed_window_5
print(f"double & add     : {double_and_add / benchmark_time:.0%}")
print(f"Montgomery ladder: {montgomery / benchmark_time:.0%}")
print(f"Base 3           : {base3 / benchmark_time:.0%}")
print(f"Fixed window 4   : {fixed_window_4 / benchmark_time:.0%}")
print(f"Fixed window 5   : {fixed_window_5 / benchmark_time:.0%}")
print(f"Sliding window   : {sliding_window / benchmark_time:.0%}")
print(f"wNAF             : {wNAF / benchmark_time:.0%}")
