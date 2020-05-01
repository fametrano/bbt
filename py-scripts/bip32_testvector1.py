#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from hashlib import sha512
from hmac import HMAC

from btclib.base58 import b58encode
from btclib.curvemult import mult
from btclib.curves import secp256k1 as ec
from btclib.secpoint import bytes_from_point
from btclib.utils import hash160

# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

# version bytes
# mainnet: 0x0488B21E public  -> xpub; 0x0488ADE4 private -> xprv
prv_version = b'\x04\x88\xAD\xE4'
pub_version = b'\x04\x88\xB2\x1E'

# master private key, master public key, chain code
path = "m"
depth = b'\x00'
parent_fingerprint = b'\x00\x00\x00\x00'
child_n = 0
child_number = child_n.to_bytes(4, byteorder='big')
metadata = depth + parent_fingerprint + child_number

seedn = 0x000102030405060708090a0b0c0d0e0f
seed = seedn.to_bytes(16, byteorder='big')
hd = HMAC(b"Bitcoin seed", seed, sha512).digest()
q = int.from_bytes(hd[:32], byteorder='big')
Q = mult(q, ec.G)
qbytes = b'\x00' + q.to_bytes(32, byteorder='big')
Qbytes = bytes_from_point(Q)
chain_code = hd[32:]

xprv = b58encode(prv_version + metadata + chain_code + qbytes, 78)
xpub = b58encode(pub_version + metadata + chain_code + Qbytes, 78)
print(path + f" : {xprv}")
print(path + f" : {xpub}")
assert xprv == b"xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"
assert xpub == b"xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8"


# first (0) hardened child
path += "/0h"
depth = b'\x01'
parent_fingerprint = hash160(Qbytes)[:4]
child_n = 0 + 0x80000000  # hardened
child_number = child_n.to_bytes(4, byteorder='big')
metadata = depth + parent_fingerprint + child_number

key = qbytes if child_number[0] > 127 else Qbytes
hd = HMAC(chain_code, key + child_number, sha512).digest()
q = (q + int.from_bytes(hd[:32], byteorder='big')) % ec.n
Q = mult(q, ec.G)
qbytes = b'\x00' + q.to_bytes(32, byteorder='big')
Qbytes = bytes_from_point(Q)
chain_code = hd[32:]

xprv = b58encode(prv_version + metadata + chain_code + qbytes, 78)
xpub = b58encode(pub_version + metadata + chain_code + Qbytes, 78)
print(path + f" : {xprv}")
print(path + f" : {xpub}")
assert xprv == b"xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7"
assert xpub == b"xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvgGDnw"

# second (1) normal grandchild
path += "/1"
depth = b'\x02'
parent_fingerprint = hash160(Qbytes)[:4]
child_n = 1 + 0x00000000  # normal
child_number = child_n.to_bytes(4, byteorder='big')
metadata = depth + parent_fingerprint + child_number

key = qbytes if child_number[0] > 127 else Qbytes
hd = HMAC(chain_code, key + child_number, sha512).digest()
q = (q + int.from_bytes(hd[:32], byteorder='big')) % ec.n
Q = mult(q, ec.G)
qbytes = b'\x00' + q.to_bytes(32, byteorder='big')
Qbytes = bytes_from_point(Q)
chain_code = hd[32:]

xprv = b58encode(prv_version + metadata + chain_code + qbytes, 78)
xpub = b58encode(pub_version + metadata + chain_code + Qbytes, 78)
print(path + f" : {xprv}")
print(path + f" : {xpub}")
assert xprv == b"xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs"
assert xpub == b"xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ"

# third (2) hardened grand-grandchild
path += "/2h"
depth = b'\x03'
parent_fingerprint = hash160(Qbytes)[:4]
child_n = 2 + 0x80000000  # hardened
child_number = child_n.to_bytes(4, byteorder='big')
metadata = depth + parent_fingerprint + child_number

key = qbytes if child_number[0] > 127 else Qbytes
hd = HMAC(chain_code, key + child_number, sha512).digest()
q = (q + int.from_bytes(hd[:32], byteorder='big')) % ec.n
Q = mult(q, ec.G)
qbytes = b'\x00' + q.to_bytes(32, byteorder='big')
Qbytes = bytes_from_point(Q)
chain_code = hd[32:]

xprv = b58encode(prv_version + metadata + chain_code + qbytes, 78)
xpub = b58encode(pub_version + metadata + chain_code + Qbytes, 78)
print(path + f" : {xprv}")
print(path + f" : {xpub}")
assert xprv == b"xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4mLTj34bhnZX7UiM"
assert xpub == b"xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7DogT5Uv6fcLW5"

# third (2) normal grand-grand-grandchild
path += "/2"
depth = b'\x04'
parent_fingerprint = hash160(Qbytes)[:4]
child_n = 2 + 0x00000000  # normal
child_number = child_n.to_bytes(4, byteorder='big')
metadata = depth + parent_fingerprint + child_number

key = qbytes if child_number[0] > 127 else Qbytes
hd = HMAC(chain_code, key + child_number, sha512).digest()
q = (q + int.from_bytes(hd[:32], byteorder='big')) % ec.n
Q = mult(q, ec.G)
qbytes = b'\x00' + q.to_bytes(32, byteorder='big')
Qbytes = bytes_from_point(Q)
chain_code = hd[32:]

xprv = b58encode(prv_version + metadata + chain_code + qbytes, 78)
xpub = b58encode(pub_version + metadata + chain_code + Qbytes, 78)
print(path + f" : {xprv}")
print(path + f" : {xpub}")
assert xprv == b"xprvA2JDeKCSNNZky6uBCviVfJSKyQ1mDYahRjijr5idH2WwLsEd4Hsb2Tyh8RfQMuPh7f7RtyzTtdrbdqqsunu5Mm3wDvUAKRHSC34sJ7in334"
assert xpub == b"xpub6FHa3pjLCk84BayeJxFW2SP4XRrFd1JYnxeLeU8EqN3vDfZmbqBqaGJAyiLjTAwm6ZLRQUMv1ZACTj37sR62cfN7fe5JnJ7dh8zL4fiyLHV"

# 1000000001th (1000000000) normal grand-grand-grand-grandchildù
path += "/1000000000"
depth = b'\x05'
parent_fingerprint = hash160(Qbytes)[:4]
child_n = 1000000000 + 0x00000000  # normal
child_number = child_n.to_bytes(4, byteorder='big')
metadata = depth + parent_fingerprint + child_number

key = qbytes if child_number[0] > 127 else Qbytes
hd = HMAC(chain_code, key + child_number, sha512).digest()
q = (q + int.from_bytes(hd[:32], byteorder='big')) % ec.n
Q = mult(q, ec.G)
qbytes = b'\x00' + q.to_bytes(32, byteorder='big')
Qbytes = bytes_from_point(Q)
chain_code = hd[32:]

xprv = b58encode(prv_version + metadata + chain_code + qbytes, 78)
xpub = b58encode(pub_version + metadata + chain_code + Qbytes, 78)
print(path + f" : {xprv}")
print(path + f" : {xpub}")
assert xprv == b"xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76"
assert xpub == b"xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
