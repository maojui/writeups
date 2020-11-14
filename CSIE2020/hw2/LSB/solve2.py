#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import *
from math import log
r = remote('140.112.31.97', 30001)

n = int(r.recvline().split(b' = ')[1])
c = int(r.recvline().split(b' = ')[1])
e = 65537

inv  = inverse(3, n)
inve = pow(inv, e, n)

flag, x = 0, 0
for i in range(int(log(n,3))):
    r.sendline(str(c))
    m = int(r.recvline().split(b' = ')[1])
    bit = (m - x) % 3
    x = inv * (x + bit) % n
    flag += bit * pow(3,i)
    c = (c * inve) % n

print(long_to_bytes(flag))
