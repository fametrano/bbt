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
from btclib.curvemult2 import _mult_base_3, _mult_fixed_window, _mult_mont_ladder, _mult_sliding_window, _mult_w_NAF
from btclib.curves import secp256k1 as ec

random.seed(42)

# setup
qs = []
for _ in range(50):
    qs.append(random.getrandbits(ec.nlen) % ec.n)

# Standard jacobian multiplication with double and add
start = time.time()
for q in qs:
    _mult_jac(q, ec.GJ, ec)
elapsed1 = time.time() - start


# Montogomery ladder jacobian multiplication
start = time.time()
for q in qs:
    _mult_mont_ladder(q, ec.GJ, ec)
elapsed_mont_ladder = time.time() - start

print("Montogomery ladder:")
print(elapsed_mont_ladder / elapsed1)

# Base 3 jacobian multiplication
start = time.time()
for q in qs:
    _mult_base_3(q, ec.GJ, ec)
elapsed_base_3 = time.time() - start

print("Base 3 jacobian multiplication:")
print(elapsed_base_3 / elapsed1)

# Fixed window method 
start = time.time()
for q in qs:
    _mult_fixed_window(q, ec.GJ, 4, ec)
elapsed_fixed_window = time.time() - start

print("Fixed window jacobian multiplication:")
print(elapsed_fixed_window / elapsed1)

# Sliding window method
start = time.time()
for q in qs:
    _mult_sliding_window(q, ec.GJ, 5, ec)
elapsed_sliding_window = time.time() - start

print("Sliding window jacobian multiplication:")
print(elapsed_sliding_window / elapsed1)

# wNAF method
start = time.time()
for q in qs:
    _mult_w_NAF(q, ec.GJ, 4, ec)
elapsed_wNAF = time.time() - start

print("wNAF jacobian multiplication:")
print(elapsed_wNAF / elapsed1)



