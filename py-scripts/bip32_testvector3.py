#!/usr/bin/python3

from hashlib import sha512
from hmac import HMAC

from btclib.base58 import b58encode
from btclib.curvemult import mult
from btclib.curves import secp256k1 as ec
from btclib.secpoint import bytes_from_point
from btclib.utils import hash160

# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

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

seedn = 0x4b381541583be4423346c643850da4b320e46a87ae3d2a4e6da11eba819cd4acba45d239319ac14f863b8d5ab5a0d0c64d2e8a1e7d1457df2e5a3c51c73235be
seed = seedn.to_bytes(64, byteorder='big')
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
assert xprv == b"xprv9s21ZrQH143K25QhxbucbDDuQ4naNntJRi4KUfWT7xo4EKsHt2QJDu7KXp1A3u7Bi1j8ph3EGsZ9Xvz9dGuVrtHHs7pXeTzjuxBrCmmhgC6"
assert xpub == b"xpub661MyMwAqRbcEZVB4dScxMAdx6d4nFc9nvyvH3v4gJL378CSRZiYmhRoP7mBy6gSPSCYk6SzXPTf3ND1cZAceL7SfJ1Z3GC8vBgp2epUt13"

# first (0) hardened child
path += "/0h"
depth = b'\x01'
parent_fingerprint = hash160(Qbytes)[:4]
child_n = 0 + 0x80000000  # hardened
child_number = child_n.to_bytes(4, 'big')
metadata = depth + parent_fingerprint + child_number

key = qbytes if child_number[0] > 127 else Qbytes
hd = HMAC(chain_code, key + child_number, sha512).digest()
p = (q + int(hd[:32].hex(), 16)) % ec.n
qbytes = b'\x00' + p.to_bytes(32, 'big')
Q = mult(p, ec.G)
Qbytes = (b'\x02' if (Q[1] % 2 == 0) else b'\x03') + Q[0].to_bytes(32, 'big')
chain_code = hd[32:]

xprv = b58encode(prv_version + metadata + chain_code + qbytes, 78)
xpub = b58encode(pub_version + metadata + chain_code + Qbytes, 78)
print(path + f" : {xprv}")
print(path + f" : {xpub}")
assert xprv == b"xprv9uPDJpEQgRQfDcW7BkF7eTya6RPxXeJCqCJGHuCJ4GiRVLzkTXBAJMu2qaMWPrS7AANYqdq6vcBcBUdJCVVFceUvJFjaPdGZ2y9WACViL4L"
assert xpub == b"xpub68NZiKmJWnxxS6aaHmn81bvJeTESw724CRDs6HbuccFQN9Ku14VQrADWgqbhhTHBaohPX4CjNLf9fq9MYo6oDaPPLPxSb7gwQN3ih19Zm4Y"
