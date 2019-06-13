#!/usr/bin/python3


with open('flag.txt', 'rb') as f:
    flag = f.read().strip()

with open('key.txt', 'rb') as f:
    key = f.read().strip()[0]

enc = bytes(c ^ key for c in flag).hex()

print(enc)
