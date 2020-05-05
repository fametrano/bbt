#!/usr/bin/env python3

# Copyright (C) 2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import secrets

from btclib import bip32, bip39, electrum

entropy = secrets.randbits(256)

bip39_mnemonic = bip39.mnemonic_from_entropy(entropy)
print()
print(bip39_mnemonic)
rxprv = bip32.mxprv_from_bip39_mnemonic(bip39_mnemonic)
rxpub = bip32.xpub_from_xprv(rxprv)
# warning: first level should always be hardened
# or any (depth=1) child private key would compromise rxprv
path = "m/0h"
xprv = bip32.derive(rxprv, path)
print(path + f" : {xprv}")

electrum_mnemonic = electrum.mnemonic_from_entropy(entropy)
print()
print(electrum_mnemonic)
mxprv = bip32.mxprv_from_electrum_mnemonic(electrum_mnemonic)
mxpub = bip32.xpub_from_xprv(mxprv)
# warning: first level should always be hardened
# or any (depth=1) child private key would compromise mxprv
path = "m/0h"
xprv = bip32.derive(mxprv, path)
print(path + f" : {xprv}")
