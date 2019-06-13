# import des
import os
import numpy as np 


def genkey():
    tmp = os.urandom(8)
    key = ''
    for ch in tmp:
        key += chr(int(ch)&0xfe)
    return key
    
# def genkey():
#     tmp = os.urandom(8)
#     key = ''
#     for ch in tmp:
#         key += chr(ord(ch)&0xfe)
#     return key

# des.gen_subkey(genkey())
# start = np.array([[[0]*48]*8]) 
# for i in range(10000):
#     start += np.array(des.gen_subkey(genkey()))

PC_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

PC_2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

def chr_to_bits(c):
    res = bin(ord(c))[2:]
    return map(int, list(res.rjust(8,'0')))

def str_to_bits(s):
    res = []
    for c in s:
        res.extend(chr_to_bits(c)) 
    return res

start = np.array([0]*56)
for i in range(1000):
    key = genkey()
    kbits = str_to_bits(key)
    start += np.array([kbits[x-1] for x in PC_1])

print( np.abs(start)-500 )
