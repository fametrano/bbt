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
from btclib.curvegroup import (
    _mult_base_3,
    _mult_fixed_window,
    _mult_jac,
    _mult_mont_ladder,
)


# setup
random.seed(42)
qs = [random.getrandbits(ec.nlen) % ec.n for _ in range(300)]


T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_jac(q, T, ec)
benchmark = time.time() - start
print("Benchmark completed")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_jac(q, T, ec)
double_and_add = time.time() - start
print(f"Double & add     : {double_and_add / benchmark:.0%}")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_mont_ladder(q, T, ec)
montgomery = time.time() - start
print(f"Montgomery ladder: {montgomery / benchmark:.0%}")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_base_3(q, T, ec)
base3 = time.time() - start
print(f"Base 3           : {base3 / benchmark:.0%}")

T = ec.GJ
w = 4
start = time.time()
for q in qs:
    T = _mult_fixed_window(q, T, ec, w)
fixed_window_4 = time.time() - start
print(f"Fixed window 4   : {fixed_window_4 / benchmark:.0%}")

T = ec.GJ
w = 5
start = time.time()
for q in qs:
    T = _mult_fixed_window(q, T, ec, w)
fixed_window_5 = time.time() - start
print(f"Fixed window 5   : {fixed_window_5 / benchmark:.0%}")


