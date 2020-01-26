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

from btclib.curve import _jac_from_aff
from btclib.curvemult import _mult_jac
from btclib.curves import secp256k1 as ec

random.seed(42)

# setup
qs = []
for _ in range(50):
    qs.append(random.getrandbits(ec.nlen) % ec.n)

start = time.time()
for q in qs:
    ec._mult_aff(q, ec.G)
elapsed1 = time.time() - start

start = time.time()
for q in qs:
    # starts from affine coordinates, ends with affine coordinates
    GJ = _jac_from_aff(ec.G)
    ec._aff_from_jac(_mult_jac(q, GJ))
elapsed2 = time.time() - start

print(elapsed2 / elapsed1)
