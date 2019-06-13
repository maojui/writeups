import string
from cryptools import *
import hashlib

key = b'deadbeef'
hash_table = {}

for c in string.printable :
    hash_table[c] = hashlib.sha256(key + bytes([ ord(c) ])).digest()[0]

enc = b'39aa1f42a72d9e3a63e89f542d323a2b8d593ac0e8aef73abc7e65bb9ea9a73e'

# 7c e5 59
enc = switchBS(n2s(int(enc,16)))

def guess(xc,c):
    return chr(ord(xc) ^ 0x1f ^ ord('F') ^ hash_table['F'] ^ hash_table[c])

flag = ''
for idx,test in enumerate(enc) :
    has = False
    for c in string.printable :
        if c == guess(test, c ):
            if has :
                flag += '?'+c+'?'
            else :
                flag += c
            has = True

EOF{15_SiMp1e_X0R_WiTH_shA256}