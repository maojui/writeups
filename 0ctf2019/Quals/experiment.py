import os
import numpy as np

ROUNDS = 8

IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

rIP = [39, 7, 47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25,32,0,40,8,48,16,56,24]

IP_1 = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

rIP_1 = [57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7, 56, 48, 40, 32, 24, 16, 8, 0, 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6]

E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

SBOX = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]], [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]], [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]], [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]], [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]], [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]], [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]], [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

PC_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

PC_2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

R = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def chr_to_bits(c):
    res = bin(ord(c))[2:]
    return map(int, list(res.rjust(8,'0')))

def str_to_bits(s):
    res = []
    for c in s:
        res.extend(chr_to_bits(c)) 
    return res

def bits_to_chr(bits):
    res = int(''.join(map(str, bits)), 2)
    return chr(res)

def bits_to_str(bits):
    res = ''
    for i in range(0, len(bits), 8):
        res += bits_to_chr(bits[i:i+8])
    return res

def xor_bits(l,r):
    res = []
    for i in range(len(l)):
        res.append(l[i]^r[i])
    return res


def encrypt_block(blk, subkeys):
    assert len(blk)==8
    bits = str_to_bits(blk)
    bits = [bits[x-1] for x in IP]
    for i in range(ROUNDS):
        left = bits[:32]
        right = bits[32:]
        left = xor_bits(left, F(right, subkeys[i]))
        bits = right + left
    bits = left + right
    bits = [bits[x-1] for x in IP_1]
    return bits_to_str(bits)

def encrypt_block_test(blk, subkeys, round):
    assert len(blk)==8
    bits = str_to_bits(blk)
    # bits = [bits[x] for x in rIP]
    bits = [bits[x-1] for x in IP]
    for i in range(round):
        left = bits[:32]
        right = bits[32:]
        left = xor_bits(left, F(right, subkeys[i]))
        bits = right + left
        # print(bits)
    bits = left + right
    bits = [bits[x-1] for x in IP_1]
    return bits_to_str(bits)

def F(hblk, subkey):
    bits = [hblk[x-1] for x in E] # 32 -> 48
    bits = xor_bits(bits, subkey) 
    res = []
    for i in range(0, len(bits), 6):   
        row = bits[i]*2+bits[i+5]
        col = bits[i+1]*8+bits[i+2]*4+bits[i+3]*2+bits[i+4]
        val = bin(SBOX[i//6][row][col])[2:]
        res.extend(map(int, list(val.rjust(4,'0'))))
    res = [res[x-1] for x in P]
    return res

def encrypt(pt, key):
    assert len(pt)%8==0
    subkeys = gen_subkey(key)
    ct = ''
    for i in range(0, len(pt), 8):
        ct += encrypt_block(pt[i:i+8], subkeys)
    return ct


def encrypt_test(pt, key, idx):
    assert len(pt)%8==0
    subkeys = gen_subkey(key)
    ct = ''
    for i in range(0, len(pt), 8):
        ct += encrypt_block_test(pt[i:i+8], subkeys, idx)
    return ct

def genkey():
    tmp = os.urandom(8)
    key = ''
    for ch in tmp:
        key += chr(ch&0xfe)
    return key


def decrypt_block(blk, subkeys):
    assert len(blk)==8
    bits = str_to_bits(blk)
    bits = [bits[x-1] for x in IP]
    for i in range(ROUNDS):
        left = bits[:32]
        right = bits[32:]
        left = xor_bits(left, F(right, subkeys[ROUNDS-1-i]))
        bits = right + left
    bits = left + right
    bits = [bits[x-1] for x in IP_1]
    return bits_to_str(bits)

def decrypt(ct, key):
    assert len(ct)%8==0
    subkeys = gen_subkey(key)
    pt = ''
    for i in range(0, len(ct), 8):
        pt += decrypt_block(ct[i:i+8], subkeys)
    return pt


def gen_subkey(key):
    kbits = str_to_bits(key)
    kbits = [kbits[x-1] for x in PC_1] 
    left = kbits[:28]
    right = kbits[28:]
    subkeys = []
    for i in range(8):
        # R = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
        left = left[R[i]:]+left[:R[i]] # left rotate shift 1 or 2
        right = right[R[i]:]+right[:R[i]]
        cur = left+right
        subkeys.append([cur[x-1] for x in PC_2])
    if subkeys[0] == subkeys[1] or subkeys[0] == subkeys[2]:
        raise Exception("Boom")
    return subkeys

key = genkey()
subkey = gen_subkey(key)

from libnum import *

# def add_delta(plaintxt, delta):
#     txt = np.array( plaintxt )
#     delta = np.array( str_to_bits(b2s(delta).rjust(8,'\x00')))

res = np.array([0]*64)
key = genkey()

# plaintxt = '\x00'*8
hex_str = lambda x : ''.join([chr(b) for b in bytes.fromhex(x)])

for i in range(1000):

    # x = hex_str('0000000000000000')
    x = ''.join(chr(r) for r in os.urandom(8))
    # dx = hex_str('42040080' + '00004000')
    dx = hex_str('00808200' + '60000000')
    tx = bits_to_str(xor_bits(str_to_bits(x),str_to_bits(dx)))

    x = str_to_bits(x)
    tx = str_to_bits(tx)
    x = [x[i] for i in rIP]
    tx = [tx[i] for i in rIP]
    x = bits_to_str(x)
    tx = bits_to_str(tx)


    test_round = 2
    y = encrypt_test(x,key,test_round)
    ty = encrypt_test(tx,key,test_round)

    y = str_to_bits(y)
    ty = str_to_bits(ty)
    y = [y[x] for x in rIP_1]
    ty = [ty[x] for x in rIP_1]

    res += np.array( y )== np.array( ty )

# print(res)
print(res[:32])
print(res[32:])
# 06000000
# [ 660  414  367  529  686  389 1000  558 1000  701  482 1000  473  569
#   693  470 1000  609  646  693  748 1000 1000  603  521  668  659  657
#   659  637 1000 1000]

# [ 652 1000  591 1000  496  437  531  479  719  636 1000  384 1000  448
#   492  625  675 1000 1000  648  412  683  661  618  487  655  711 1000
#  1000  679  644  465]


[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]