#!/usr/bin/python3

import hmac

from btclib.base58 import b58encode
from btclib.curvemult import mult
from btclib.curves import secp256k1 as ec
from btclib.secpoint import bytes_from_point
from btclib.utils import hash160

# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

# version bytes
# mainnet: 0x0488B21E public  -> xpub; 0x0488ADE4 private -> xprv
# testnet: 0x043587CF public         ; 0x04358394 private
xprvn = 0x0488ADE4
xprv = xprvn.to_bytes(4, "big")
xpubn = 0x0488B21E
xpub = xpubn.to_bytes(4, "big")

seed = 0x4B381541583BE4423346C643850DA4B320E46A87AE3D2A4E6DA11EBA819CD4ACBA45D239319AC14F863B8D5AB5A0D0C64D2E8A1E7D1457DF2E5A3C51C73235BE
seed_bytes = 64
print("Seed:", hex(seed), "\nbytes:", seed_bytes)

# ==master ext private key==
# depth: 0x00 for master nodes, 0x01 for level-1 derived keys, ...
depth = b"\x00"
# This is ser32(i) for i in xi = xpar/i, with xi the key being serialized. (0x00000000 if master key)
child_number = b"\x00\x00\x00\x00"
# the fingerprint of the parent's public key (0x00000000 if master key)
fingerprint = b"\x00\x00\x00\x00"
idf = depth + fingerprint + child_number

# master private key, master public key, chain code
hd = hmac.digest(b"Bitcoin seed", seed.to_bytes(seed_bytes, "big"), "sha512")
qbytes = hd[:32]
p = int(qbytes.hex(), 16) % ec.n
qbytes = b"\x00" + p.to_bytes(32, "big")
Q = mult(p, ec.G)
Qbytes = bytes_from_point(Q)
chain_code = hd[32:]

# extended keys
ext_prv = b58encode(xprv + idf + chain_code + qbytes)
print("\nm")
print(ext_prv)
ext_pub = b58encode(xpub + idf + chain_code + Qbytes)
print("M")
print(ext_pub)
assert (
    ext_prv
    == b"xprv9s21ZrQH143K25QhxbucbDDuQ4naNntJRi4KUfWT7xo4EKsHt2QJDu7KXp1A3u7Bi1j8ph3EGsZ9Xvz9dGuVrtHHs7pXeTzjuxBrCmmhgC6"
), "failure"
assert (
    ext_pub
    == b"xpub661MyMwAqRbcEZVB4dScxMAdx6d4nFc9nvyvH3v4gJL378CSRZiYmhRoP7mBy6gSPSCYk6SzXPTf3ND1cZAceL7SfJ1Z3GC8vBgp2epUt13"
), "failure"

# ==first (0) hardened child==
depth = b"\x01"
child_n = 0 + 0x80000000  # hardened
child_number = child_n.to_bytes(4, "big")
fingerprint = hash160(Qbytes)[:4]
idf = depth + fingerprint + child_number

key = qbytes if child_number[0] > 127 else Qbytes
hd = hmac.digest(chain_code, key + child_number, "sha512")
p = (p + int(hd[:32].hex(), 16)) % ec.n
qbytes = b"\x00" + p.to_bytes(32, "big")
Q = mult(p, ec.G)
Qbytes = (b"\x02" if (Q[1] % 2 == 0) else b"\x03") + Q[0].to_bytes(32, "big")
chain_code = hd[32:]

ext_prv = b58encode(xprv + idf + chain_code + qbytes)
print("\nm/0'")
print(ext_prv)
ext_pub = b58encode(xpub + idf + chain_code + Qbytes)
print("M/0'")
print(ext_pub)
assert (
    ext_prv
    == b"xprv9uPDJpEQgRQfDcW7BkF7eTya6RPxXeJCqCJGHuCJ4GiRVLzkTXBAJMu2qaMWPrS7AANYqdq6vcBcBUdJCVVFceUvJFjaPdGZ2y9WACViL4L"
), "failure"
assert (
    ext_pub
    == b"xpub68NZiKmJWnxxS6aaHmn81bvJeTESw724CRDs6HbuccFQN9Ku14VQrADWgqbhhTHBaohPX4CjNLf9fq9MYo6oDaPPLPxSb7gwQN3ih19Zm4Y"
), "failure"
