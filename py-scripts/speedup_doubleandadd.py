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
    _mult_aff,
    _mult_jac,
    _mult_recursive_aff,
    _mult_recursive_jac,
)

# setup
random.seed(42)
qs = [random.getrandbits(ec.nlen) % ec.n for _ in range(100)]

start = time.time()
for q in qs:
    # starts from affine coordinates, ends with affine coordinates
    ec._aff_from_jac(_mult_jac(q, ec.GJ, ec))
benchmark = time.time() - start
print("Benchmark completed")

start = time.time()
for q in qs:
    _mult_recursive_aff(q, ec.G, ec)
recursive_aff = time.time() - start
print(f"Recursive aff       : {recursive_aff / benchmark:.0%}")

start = time.time()
for q in qs:
    ec._aff_from_jac(_mult_recursive_jac(q, ec.GJ, ec))
recursive_jac = time.time() - start
print(f"Recursive jac       : {recursive_jac / benchmark:.0%}")

start = time.time()
for q in qs:
    _mult_aff(q, ec.G, ec)
double_add_aff = time.time() - start
print(f"Double and add aff  : {double_add_aff / benchmark:.0%}")

start = time.time()
for q in qs:
    ec._aff_from_jac(_mult_jac(q, ec.GJ, ec))
double_add_jac = time.time() - start
print(f"Double and add jac  : {double_add_jac / benchmark:.0%}")
