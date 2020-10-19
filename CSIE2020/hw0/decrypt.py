#!/usr/bin/env python3
import time 
import string
import random 
from typing import List
from io import BufferedReader
from forbiddenfruit import curse 

def s2b(data, size=4):
    return [int.from_bytes(data[idx:idx+size], 'big') for idx in range(0, len(data), size)]

def qq(data, size=4):
    return b''.join([element.to_bytes(size, 'big') for element in data])

def _encrypt(vec: List[int], key: List[int]):
    it, delta, mask = 0, 0xFACEB00C, 0xffffffff
    for _ in range(32):
        it = it + delta & mask
        vec[0] = vec[0] + ((vec[1] << 4) + key[0] & mask ^ (vec[1] + it) & mask ^ (vec[1] >> 5) + key[1] & mask) & mask
        vec[1] = vec[1] + ((vec[0] << 4) + key[2] & mask ^ (vec[0] + it) & mask ^ (vec[0] >> 5) + key[3] & mask) & mask
    return vec

def _decrypt(vec: List[int], key: List[int]):
    it, delta, mask = 0x59D60180, 0xFACEB00C, 0xffffffff
    for _ in range(32):
        vec[1] = vec[1] - ((vec[0] << 4) + key[2] & mask ^ (vec[0] + it) & mask ^ (vec[0] >> 5) + key[3] & mask) & mask
        vec[0] = vec[0] - ((vec[1] << 4) + key[0] & mask ^ (vec[1] + it) & mask ^ (vec[1] >> 5) + key[1] & mask) & mask
        it = it - delta & mask
    return vec

def decrypt(cipher: bytes, key: bytes):
    plaintxt = b''
    for idx in range(0, len(cipher), 8):
        plaintxt += qq(_decrypt(s2b(cipher[idx:idx+8]), s2b(key)))
    return plaintxt

def encrypt(plaintxt: bytes, key: bytes):
    cipher = b''
    for idx in range(0, len(plaintxt), 8):
        cipher += qq(_encrypt(s2b(plaintxt[idx:idx+8]), s2b(key)))
    return cipher

for i in range(1599977589, 0, -1):
    random.seed(i)
    key = random.getrandbits(128).to_bytes(16, 'big')
    cipher = bytes.fromhex("77f905c39e36b5eb0deecbb4eb08e8cb")
    _flag = decrypt(cipher, key)
    if all(chr(b) in string.printable for b in _flag) :
        print(f'{i}, {_flag}')
        exit()
        