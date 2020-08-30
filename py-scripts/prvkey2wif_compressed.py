#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from hashlib import sha256

from btclib import base58

# https://en.bitcoin.it/wiki/Wallet_import_format
print("\n****** Private ECDSA Key to WIF ******")

print("\n*** [1] Private ECDSA Key:")
q = 0xC28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D
print(hex(q))

print("\n*** [2] payload (compressed):")
payload = b"\x80" + q.to_bytes(32, "big") + b"\x01"
print(payload.hex())

print("\n*** [3] SHA-256 hashing of the SHA-256:")
h1 = sha256(payload).digest()
print(h1.hex())

print("\n*** [4] SHA-256 hashing of the SHA-256:")
h2 = sha256(h1).digest()
print(h2.hex())

print("\n*** [5] First 4 bytes of the double SHA-256 used as checksum:")
print(h2[:4].hex())

print("\n*** [6] checksum added at the end of extended key:")
checksummed_payload = payload + h2[:4]
print(checksummed_payload.hex())

print("\n*** [7] Base58 encoding")
wif = base58._b58encode(checksummed_payload)
print(wif)
assert wif == b"KwdMAjGmerYanjeui5SHS7JkmpZvVipYvB2LJGU1ZxJwYvP98617", "failure"
assert (
    base58.b58encode(payload) == b"KwdMAjGmerYanjeui5SHS7JkmpZvVipYvB2LJGU1ZxJwYvP98617"
), "failure"

print("\n****** WIF to private key ******")

print("\n*** [1] Base58 WIF")
print(wif)
compressed = len(wif) - 51
print("compressed" if (compressed == 1) else "uncompressed")

print("\n*** [2] Base58 decoding")
checksummed_payload = base58._b58decode(wif)
print(checksummed_payload.hex())

print("\n*** [3] Extended key (checksum verified)")
payload, checksum = checksummed_payload[:-4], checksummed_payload[-4:]
verified = sha256(sha256(payload).digest()).digest()[:4] == checksum
print(payload.hex() + " (" + ("true" if verified else "false") + ")")
print(base58.b58decode(wif).hex())

print("\n*** [4] Private key")
p2 = payload[1:-1].hex() if compressed else payload[1:].hex()
assert int(p2, 16) == q, "failure"
print(p2)
