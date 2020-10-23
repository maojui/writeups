#!/usr/bin/env python3
import random
from Crypto.Util.number import *
from gmpy2 import next_prime

def pad(data, block_size):
    padlen = block_size - len(data) - 2
    if padlen < 8:
        raise ValueError
    return b'\x00' + bytes([random.randint(1, 255) for _ in range(padlen)]) + b'\x00' + data

FLAG = open('./flag', 'rb').read()

p = getPrime(512)
q1 = next_prime(2 * p)
q2 = next_prime(3 * q1)

n = p * q1 * q2
e = 65537

m = bytes_to_long(pad(FLAG, 192))
c = pow(m, e, n)
print(f'n = {n}')
print(f'c = {c}')
