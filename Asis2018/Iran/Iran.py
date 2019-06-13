#!/usr/bin/python

from Crypto.PublicKey import RSA
import gmpy
from secret import r, s, p, q, FLAG

assert ((p-1) % r)**2 + ((q-1) % s)**4 + ((r**3 - 1) % p)**8 + ((s**3 - 1) % q)**16 == 0
assert gmpy.is_prime(r) + gmpy.is_prime(s) + gmpy.is_prime(p) + gmpy.is_prime(q) == 4

def keysaz(a, b):
    e, n = 65537, a * b
    d = gmpy.invert(e, (a-1)*(b-1))
    key = RSA.construct((long(n), long(e), long(d)))
    return key

key_0, key_1 = keysaz(gmpy.next_prime(r+s), gmpy.next_prime((r+s)<<2)), keysaz(p, q)
pkey_0, pkey_1 = key_0.publickey().exportKey(), key_1.publickey().exportKey()

print pkey_0 
enc_0 = key_0.encrypt(FLAG[:18], 1L)[0]
print 'enc_0 =\n', enc_0.encode('base64')

print pkey_1
enc_1 = key_1.encrypt(FLAG[18:], 1L)[0]
print 'enc_1 =\n', enc_1.encode('base64')

