# plaintxt, ciphertxt = [], []
# cipher = open('data','rb').read()
# for i in range( 0, len(cipher), 16) :
#     plaintxt.append(cipher[i*16:i*16+8])
#     ciphertxt.append(cipher[i*16+8:i*16+16])
rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a]

sbox = [62, 117, 195, 179, 20, 210, 41, 66, 116, 178, 152, 143, 75, 105, 254, 1, 158, 95, 101, 175, 191, 166, 36, 24, 50, 39, 190, 120, 52, 242, 182, 185, 61, 225, 140, 38, 150, 80, 19, 109, 246, 252, 40, 13, 65, 236, 124, 186, 214, 86, 235, 100, 97, 49, 197, 154, 176, 199, 253, 69, 88, 112, 139, 77, 184, 45, 133, 104, 15, 54, 177, 244, 160, 169, 82, 148, 73, 30, 229, 35, 79, 137, 157, 180, 248, 163, 241, 231, 81, 94, 165, 9, 162, 233, 18, 85, 217, 84, 7, 55, 63, 171, 56, 118, 237, 132, 136, 22, 90, 221, 103, 161, 205, 11, 255, 14, 122, 47, 71, 201, 99, 220, 83, 74, 173, 76, 144, 16, 155, 126, 60, 96, 44, 234, 17, 215, 107, 138, 159, 183, 251, 3, 198, 0, 89, 170, 131, 151, 219, 29, 230, 32, 187, 125, 134, 64, 12, 202, 164, 247, 25, 223, 222, 119, 174, 67, 147, 146, 206, 51, 243, 53, 121, 239, 68, 130, 70, 203, 211, 111, 108, 113, 8, 106, 57, 240, 21, 93, 142, 238, 167, 5, 128, 72, 189, 192, 193, 92, 10, 204, 87, 145, 188, 172, 224, 226, 207, 27, 218, 48, 33, 28, 123, 6, 37, 59, 4, 102, 114, 91, 23, 209, 34, 42, 2, 196, 141, 208, 181, 245, 43, 78, 213, 216, 232, 46, 98, 26, 212, 58, 115, 194, 200, 129, 227, 249, 127, 149, 135, 228, 31, 153, 250, 156, 168, 110]

ptable = [
    0, 8, 16, 24, 32, 40, 48, 56,
    1, 9, 17, 25, 33, 41, 49, 57,
    2, 10, 18, 26, 34, 42, 50, 58,
    3, 11, 19, 27, 35, 43, 51, 59,
    4, 12, 20, 28, 36, 44, 52, 60,
    5, 13, 21, 29, 37, 45, 53, 61,
    6, 14, 22, 30, 38, 46, 54, 62,
    7, 15, 23, 31, 39, 47, 55, 63
] 

for insum in range(1,256):
    for outsum in range(1,256):
        bias = sum((bin(x&insum).count('1') - bin(sbox[x]&outsum).count('1')) % 2 for x in range(256)) - 128
        if abs(bias) > 50:
            print('+'.join([f'x{i}' for i in range(8) if insum&(2**i)]) + ' -> ' + '+'.join([f'y{i}' for i in range(8) if outsum&(2**i)]),bias)


from cryptools import *

def permutation(a):
    assert len(a) == 8
    bits = s2b(a)
    bits = [bits[ptable[i]] for i in range(64)]
    bits = ''.join(bits)
    return b2s(bits)

import sympy
# Some precomputations of the P-box to use (byte,bit) indexing
pt = [[None for i in range(8)] for j in range(8)]
for i in range(8):
    for j in range(8):
        c = ['\x00'] *8
        c[i] = chr(1<<j)
        d = permutation(c)
        i2 = None
        for k in range(8):
            if d[k] != '\x00':
                assert i2 is None
                i2 = k
        j2 = None
        for k in range(8):
            if (ord(d[i2])&(1<<k)) != 0:
                assert j2 is None
                j2 = k
        pt[i][j] = (i2,j2)

print(pt[0])
K = sympy.IndexedBase('K')
P = sympy.IndexedBase('P')
U4 = sympy.IndexedBase('U4')

def k(r, i, b):
    # all key bits xor must be the same, guess it 0
    return 0

def p(i, b):
    # plain-text bits
    return P[i, b]

def u(r, i, b):
    # this is the input of the last S-box, leave it as it is
    if r == 4:
        return U4[i, b]
    # These numbers are from the S-box biases where there is only a single input bit involved, map them to output bits
    return sum(map(lambda x: v(r, i, x), [[0,1,2,7], [0,1,3,4,7], [0,1,2,3,4,6,7], [1,4,5,7], [0,2,4,5,6], [0,1,2,3,4], [1,7], [0,4]][b]))

def v(r, i, b):
    # From the output of an S-box we can get to the input of the next S-box by using the permutations (and some key bits)
    return k(r+1, pt[i][b][0], pt[i][b][1])+u(r+1, pt[i][b][0], pt[i][b][1])

def x(b):
    # Input of the first S-box is the plaintext bit ^ a key bit
    return p(0, b)+k(1, 0, b)

def y(b):
    # Output of the first S-box
    return v(1, 0, b)

def key_inv(rnd, r5):
    r4b = bytearray(r5[i]^r5[4+i] for i in range(4))
    r4a = bytearray(r5[i]^sbox[r4b[(i+1)%4]] ^ (rcon[rnd] if i == 0 else 0) for i in range(4))
    return r4a + r4b

r5 = bytearray([130, 167, 150, 65, 235, 239, 194, 40])
r4 = key_inv(4, r5)
r3 = key_inv(3, r4)
r2 = key_inv(2, r3)
r1 = key_inv(1, r2)

print('flag{%s}' % ''.join([hex(c)[2:].rjust(2,'0') for c in r1]) )