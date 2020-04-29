#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from btclib.base58address import p2pkh, p2wpkh_p2sh
from btclib.base58wif import wif_from_prvkey
from btclib.bech32address import p2wpkh
from btclib.bms import serialize, sign, verify
from btclib.to_prvkey import prvkey_info_from_prvkey
from btclib.to_pubkey import pubkey_info_from_prvkey

msg = "Paolo is afraid of ephemeral random numbers"
print("\n0. Message:", msg)

wif = b'Kx45GeUBSMPReYQwgXiKhG9FzNXrnCeutJp4yjTd5kKxCitadm3C'
print("1. Compressed WIF:", wif.decode())
pubkey, network = pubkey_info_from_prvkey(wif)

print("2. Addresses")
address1 = p2pkh(pubkey)
print("      p2pkh:", address1.decode())
address2 = p2wpkh_p2sh(pubkey)
print("p2wpkh_p2sh:", address2.decode())
address3 = p2wpkh(pubkey)
print("     p2wpkh:", address3.decode())


print("\n3. Sign message with no address (or with compressed p2pkh address):")
sig1 = sign(msg, wif)
print(f"rf1: {sig1[0]}")
print(f" r1: {hex(sig1[1]).upper()}")
print(f" s1: {hex(sig1[2]).upper()}")

bsmsig1 = serialize(*sig1)
print("4. Serialized signature:")
print(bsmsig1.decode())

print("5. Verify signature")
print("Bitcoin Core p2pkh  :", verify(msg, address1, sig1))
print("Electrum p2wpkh_p2sh:", verify(msg, address2, sig1))
print("Electrum p2wpkh     :", verify(msg, address3, sig1))


print("\n3. Sign message with p2wpkh_p2sh address (BIP137):")
sig2 = sign(msg, wif, address2)
print(f"rf2: {sig2[0]}")
print(f" r2: {hex(sig2[1]).upper()}")
print(f" s2: {hex(sig2[2]).upper()}")

bsmsig2 = serialize(*sig2)
print("4. Serialized signature:")
print(bsmsig2.decode())

print("5. Verify signature")
print("Bitcoin Core p2pkh:", verify(msg, address1, sig2))
print("BIP137 p2wpkh_p2sh:", verify(msg, address2, sig2))
print("BIP137 p2wpkh     :", verify(msg, address3, sig2))


print("\n3. Sign message with p2wpkh address (BIP137):")
sig3 = sign(msg, wif, address3)
print(f"rf3: {sig3[0]}")
print(f" r3: {hex(sig3[1]).upper()}")
print(f" s3: {hex(sig3[2]).upper()}")

bsmsig3 = serialize(*sig3)
print("4. Serialized signature:")
print(bsmsig3.decode())

print("5. Verify signature")
print("Bitcoin Core p2pkh:", verify(msg, address1, sig3))
print("BIP137 p2wpkh_p2sh:", verify(msg, address2, sig3))
print("BIP137 p2wpkh     :", verify(msg, address3, sig3))


# uncompressed WIF / P2PKH address
q, network, _ = prvkey_info_from_prvkey(wif)
wif2 = wif_from_prvkey(q, network, compressed=False)
print("\n1. Uncompressed WIF          :", wif2.decode())
pubkey, network = pubkey_info_from_prvkey(wif2)

address4 = p2pkh(pubkey)
print("2. Uncompressed P2PKH address:", address4.decode())

print("3. Sign message with uncompressed p2pkh:")
sig4 = sign(msg, wif2, address4)
print(f"rf4: {sig4[0]}")
print(f" r4: {hex(sig4[1]).upper()}")
print(f" s4: {hex(sig4[2]).upper()}")

bsmsig4 = serialize(*sig4)
print("4. Serialized signature:")
print(bsmsig4.decode())

print("5. Verify signature")
print("Bitcoin Core compressed p2pkh  :", verify(msg, address1, sig4))
print("Electrum p2wpkh_p2sh           :", verify(msg, address2, sig4))
print("Electrum p2wpkh                :", verify(msg, address3, sig4))
print("Bitcoin Core uncompressed p2pkh:", verify(msg, address4, sig4))
