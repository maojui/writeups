#!/usr/bin/python3
import hashlib
import time


with open('flag.txt', 'rb') as f:
    flag = f.read().strip()
key = hashlib.sha256(str(int(time.time())).encode()).digest()

assert len(flag) <= len(key)

enc = bytes(c ^ k for c, k in zip(flag, key)).hex()

print(enc)
a = time.time()

while True :
    a += 1
    key = hashlib.sha256(str(int(a)).encode()).digest()
    flag = bytes.fromhex(bytes(c ^ k for c, k in zip(enc, key)).hex())
    if b"EOF{" in flag and b'}' in flag:
        print(a)
        print(flag)
# 1547728039
# EOF{&Co0l_Y0u_kn0w_h0w2d3c2ypt&}