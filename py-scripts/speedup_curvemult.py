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
    _mult,
    _mult_base_3,
    _mult_fixed_window,
    _mult_jac,
    _mult_mont_ladder,
    cached_multiples,
    _MAX_W
)
from btclib.curvegroup2 import _mult_sliding_window, _mult_w_NAF

# setup
random.seed(42)
qs = [random.getrandbits(ec.nlen) % ec.n for _ in range(300)]
cached_multiples(ec.GJ, ec)

gen_only = True

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult(q, ec.GJ, ec) if gen_only else _mult(q, T, ec)
benchmark = time.time() - start
print("benchmark completed")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_jac(q, ec.GJ, ec) if gen_only else _mult_jac(q, T, ec)
double_and_add = time.time() - start
print("double_and_add completed")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_mont_ladder(q, ec.GJ, ec) if gen_only else _mult_mont_ladder(q, T, ec)
montgomery = time.time() - start
print("montgomery completed")

cached_multiples(ec.GJ, ec)
T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_base_3(q, ec.GJ, ec) if gen_only else _mult_base_3(q, T, ec)
base3 = time.time() - start
print("base3 completed")

cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 4
start = time.time()
for q in qs:
    T = _mult_fixed_window(q, ec.GJ, ec, w) if gen_only else _mult_fixed_window(q, T, ec, w)
fixed_window_4 = time.time() - start
print(f"fixed_window_{w} completed")

cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 5
start = time.time()
for q in qs:
    T = _mult_fixed_window(q, ec.GJ, ec, w) if gen_only else _mult_fixed_window(q, T, ec, w)
fixed_window_5 = time.time() - start
print(f"fixed_window_{w} completed")

cached_multiples(ec.GJ, ec)
T = ec.GJ
w = _MAX_W
start = time.time()
for q in qs:
    T = _mult_fixed_window(q, ec.GJ, ec, w, True) if gen_only else _mult_fixed_window(q, T, ec, w, True)
fixed_window_ca = time.time() - start
print(f"fixed_window_{w} cached completed")

cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 4
start = time.time()
for q in qs:
    T = _mult_sliding_window(q, ec.GJ, ec, 5) if gen_only else _mult_sliding_window(q, T, ec, w)
sliding_window_4 = time.time() - start
print(f"sliding_window_{w} completed")

cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 5
start = time.time()
for q in qs:
    T = _mult_sliding_window(q, ec.GJ, ec, 5) if gen_only else _mult_sliding_window(q, T, ec, w)
sliding_window_5 = time.time() - start
print(f"sliding_window_{w} completed")

cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 4
start = time.time()
for q in qs:
    T = _mult_w_NAF(q, ec.GJ, ec, 4) if gen_only else _mult_w_NAF(q, T, ec, w)
wNAF_4 = time.time() - start
print(f"wNAF_{w} completed")

cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 5
start = time.time()
for q in qs:
    T = _mult_w_NAF(q, ec.GJ, ec, 4) if gen_only else _mult_w_NAF(q, T, ec, w)
wNAF_5 = time.time() - start
print(f"wNAF_{w} completed")

print("-----")
print(f"double & add     : {double_and_add / benchmark:.0%}")
print(f"Montgomery ladder: {montgomery / benchmark:.0%}")
print(f"Base 3           : {base3 / benchmark:.0%}")
print(f"Fixed window 4   : {fixed_window_4 / benchmark:.0%}")
print(f"Fixed window 5   : {fixed_window_5 / benchmark:.0%}")
print(f"Fixed window ca  : {fixed_window_ca / benchmark:.0%}")
print(f"Sliding window 4 : {sliding_window_4 / benchmark:.0%}")
print(f"Sliding window 5 : {sliding_window_5 / benchmark:.0%}")
print(f"wNAF 4           : {wNAF_4 / benchmark:.0%}")
print(f"wNAF 5           : {wNAF_5 / benchmark:.0%}")
