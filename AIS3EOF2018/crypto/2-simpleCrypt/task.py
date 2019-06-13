#!/usr/bin/python3
import hashlib

with open('flag.txt', 'rb') as f:
    flag = f.read().strip()
key = b'deadbeef'

print(hashlib.sha256(flag).hexdigest())

flag = list(flag)
enc = flag[:]

for i, c in enumerate(flag):
    k = hashlib.sha256(key + bytes([c])).digest()[0]
    for j in range(len(enc)):
        if i != j:
            enc[j] ^= k

enc = bytes(enc).hex()
print(enc)
 