
import random
import time
from collections import deque

from btclib import base58

random.seed(42)

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE58_ALPHABET_LIST = list(BASE58_ALPHABET)

__digits = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__digits_list = list(__digits[i:i+1] for i in __digits)
__base  = 58

def encode_from_int1(i):
    encoded = deque()
    while i:
        i, idx = divmod(i, __base)
        encoded.appendleft(__digits[idx:idx+1])

    encoded = b''.join(encoded)

def encode_from_int2(i):
    encoded = deque()
    while i:
        i, idx = divmod(i, __base)
        encoded.appendleft(__digits_list[idx])

    encoded = b''.join(encoded)

def encode_from_int(i: int) -> bytes:
    """Encode an integer using Base58"""

    if i == 0:
        return __digits[0:1]

    result = b""
    while i:
        i, idx = divmod(i, __base)
        result = __digits[idx:idx+1] + result

    return result

ints = []
for _ in range(500000):
    ints.append(random.getrandbits(256))

start = time.time()
for i in ints:
    encode_from_int1(i)
elapsed1 = time.time() - start

start = time.time()
for i in ints:
    encode_from_int2(i)
elapsed2 = time.time() - start

print(elapsed1 / elapsed2)
