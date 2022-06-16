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

from btclib.ecc.curve import secp256k1 as ec
from btclib.curvegroup import (
    _mult,
    _mult_base_3,
    _mult_fixed_window,
    _mult_fixed_window_cached,
    _mult_jac,
    _mult_mont_ladder,
    cached_multiples,
    cached_multiples_fixwind,
)
from btclib.curvegroup2 import (
    _mult_endomorphism_secp256k1,
    _mult_sliding_window,
    _mult_w_NAF,
)

# setup
random.seed(42)
qs = [random.getrandbits(ec.nlen) % ec.n for _ in range(300)]

gen_only = True
print("generator only") if gen_only else print("random points")

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
start = time.time()
for q in qs:
    T = _mult(q, ec.GJ, ec) if gen_only else _mult(q, T, ec)
benchmark = time.time() - start
print("Benchmark completed", cached_multiples.cache_info())

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_jac(q, ec.GJ, ec) if gen_only else _mult_jac(q, T, ec)
double_and_add = time.time() - start
print(f"Double & add     : {double_and_add / benchmark:.0%}")

T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_mont_ladder(q, ec.GJ, ec) if gen_only else _mult_mont_ladder(q, T, ec)
montgomery = time.time() - start
print(f"Montgomery ladder: {montgomery / benchmark:.0%}")

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
start = time.time()
for q in qs:
    T = _mult_base_3(q, ec.GJ, ec) if gen_only else _mult_base_3(q, T, ec)
base3 = time.time() - start
print(f"Base 3           : {base3 / benchmark:.0%}", cached_multiples.cache_info())

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 4
cached = False
start = time.time()
for q in qs:
    T = (
        _mult_fixed_window(q, ec.GJ, ec, w, cached)
        if gen_only
        else _mult_fixed_window(q, T, ec, w, cached)
    )
fixed_window_4 = time.time() - start
print(
    f"Fixed window 4   : {fixed_window_4 / benchmark:.0%}",
    cached_multiples.cache_info(),
)

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 5
cached = False
start = time.time()
for q in qs:
    T = (
        _mult_fixed_window(q, ec.GJ, ec, w, cached)
        if gen_only
        else _mult_fixed_window(q, T, ec, w, cached)
    )
fixed_window_5 = time.time() - start
print(
    f"Fixed window 5   : {fixed_window_5 / benchmark:.0%}",
    cached_multiples.cache_info(),
)

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 4
cached = True
start = time.time()
for q in qs:
    T = (
        _mult_fixed_window(q, ec.GJ, ec, w, cached)
        if gen_only
        else _mult_fixed_window(q, T, ec, w, cached)
    )
fixed_window_4_ca = time.time() - start
print(
    f"Fixed window 4 ca: {fixed_window_4_ca / benchmark:.0%}",
    cached_multiples.cache_info(),
)

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 5
cached = True
start = time.time()
for q in qs:
    T = (
        _mult_fixed_window(q, ec.GJ, ec, w, cached)
        if gen_only
        else _mult_fixed_window(q, T, ec, w, cached)
    )
fixed_window_5_ca = time.time() - start
print(
    f"Fixed window 5 ca: {fixed_window_5_ca / benchmark:.0%}",
    cached_multiples.cache_info(),
)

cached_multiples_fixwind.cache_clear()
cached_multiples_fixwind(ec.GJ, ec)
T = ec.GJ
start = time.time()
for q in qs:
    T = (
        _mult_fixed_window_cached(q, ec.GJ, ec)
        if gen_only
        else _mult_fixed_window_cached(q, T, ec)
    )
fixed_window_cached = time.time() - start
print(
    f"New Fixed window : {fixed_window_cached / benchmark:.0%}",
    cached_multiples_fixwind.cache_info(),
)

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 4
start = time.time()
for q in qs:
    T = (
        _mult_sliding_window(q, ec.GJ, ec, 5)
        if gen_only
        else _mult_sliding_window(q, T, ec, w)
    )
sliding_window_4 = time.time() - start
print(
    f"Sliding window 4 : {sliding_window_4 / benchmark:.0%}",
    cached_multiples.cache_info(),
)

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 5
start = time.time()
for q in qs:
    T = (
        _mult_sliding_window(q, ec.GJ, ec, 5)
        if gen_only
        else _mult_sliding_window(q, T, ec, w)
    )
sliding_window_5 = time.time() - start
print(
    f"Sliding window 5 : {sliding_window_5 / benchmark:.0%}",
    cached_multiples.cache_info(),
)

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 4
start = time.time()
for q in qs:
    T = _mult_w_NAF(q, ec.GJ, ec, 4) if gen_only else _mult_w_NAF(q, T, ec, w)
wNAF_4 = time.time() - start
print(f"wNAF 4           : {wNAF_4 / benchmark:.0%}", cached_multiples.cache_info())

cached_multiples.cache_clear()
cached_multiples(ec.GJ, ec)
T = ec.GJ
w = 5
start = time.time()
for q in qs:
    T = _mult_w_NAF(q, ec.GJ, ec, 4) if gen_only else _mult_w_NAF(q, T, ec, w)
wNAF_5 = time.time() - start
print(f"wNAF 5           : {wNAF_5 / benchmark:.0%}", cached_multiples.cache_info())


T = ec.GJ
start = time.time()
for q in qs:
    T = (
        _mult_endomorphism_secp256k1(q, ec.GJ, ec)
        if gen_only
        else _mult_endomorphism_secp256k1(q, T, ec)
    )
endomorphism1 = time.time() - start
print(f"Mult eff end     : {endomorphism1 / benchmark:.0%}")
