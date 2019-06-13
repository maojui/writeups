#!/usr/bin/env python
# coding=utf-8

from secret import secret

rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a]
sbox = [103, 172, 53, 159, 102, 168, 133, 197, 174, 182, 41, 164, 220, 58, 118, 63, 161, 50, 89, 242, 253, 74, 250, 119, 108, 122, 120, 216, 60, 208, 178, 20, 180, 187, 117, 213, 48, 90, 218, 46, 190, 188, 111, 252, 56, 77, 169, 232, 135, 72, 44, 115, 130, 57, 96, 155, 105, 181, 83, 0, 204, 139, 9, 7, 138, 23, 145, 97, 185, 13, 254, 69, 24, 34, 158, 76, 222, 165, 2, 247, 226, 6, 183, 116, 206, 21, 225, 210, 219, 36, 129, 100, 141, 62, 198, 28, 207, 84, 184, 99, 160, 215, 52, 73, 153, 42, 191, 26, 162, 194, 235, 81, 238, 110, 43, 214, 234, 221, 70, 80, 148, 176, 251, 245, 151, 244, 132, 14, 29, 94, 137, 131, 189, 31, 231, 47, 68, 8, 11, 249, 243, 37, 203, 200, 202, 255, 236, 112, 51, 10, 98, 79, 19, 59, 228, 177, 192, 75, 85, 45, 121, 27, 147, 179, 1, 201, 123, 18, 167, 166, 239, 146, 49, 196, 163, 109, 15, 143, 144, 150, 65, 106, 25, 124, 54, 241, 16, 92, 227, 217, 104, 173, 223, 86, 113, 39, 157, 199, 126, 71, 33, 61, 38, 142, 87, 22, 237, 152, 55, 212, 248, 175, 149, 170, 246, 88, 17, 64, 209, 171, 240, 224, 154, 211, 78, 93, 205, 114, 136, 12, 40, 101, 5, 95, 233, 35, 186, 195, 230, 127, 91, 229, 193, 32, 30, 4, 140, 66, 134, 128, 125, 82, 3, 67, 107, 156]
ptable = [
    16, 19, 23, 9, 22, 20, 21, 17, 
    40, 43, 44, 47, 41, 45, 57, 42, 
    36, 32, 38, 33, 55, 37, 34, 35, 
    50, 53, 48, 52, 39, 54, 49, 51, 
    10, 11, 14, 8, 13, 15, 18, 12, 
    0, 7, 2, 3, 4, 1, 5, 31, 
    63, 46, 58, 62, 61, 59, 56, 60, 
    6, 29, 25, 24, 30, 27, 28, 26
]

def s2b(s):
    return map(int, format(int(str(s).encode('hex'), 16), '0{}b'.format(8*len(s))))

def b2s(b):
    return bytearray.fromhex(format(reduce(lambda x,y: 2*x+y, b), '0{}x'.format(len(b)/4)))

def addkey(a, b):
    global flag
    return bytearray(i^j for i,j in zip(a, b))

def substitute(a):
    return bytearray(sbox[i] for i in a)

def permutation(a):
    assert len(a) == 8
    bits = s2b(a)
    bits = [bits[ptable[i]] for i in xrange(64)]
    return b2s(bits)

class zer0TC(object):
    '''0ops Toy Cipher'''

    def __init__(self, key, key_size=8, rounds=5):
        assert len(key) == key_size
        self.key = key
        self.key_size = key_size
        self.rounds = rounds
        self.key_schedule()

    def key_schedule(self):
        roundkey = bytearray(self.key)
        tmp = roundkey[-4:]
        for i in xrange(1, self.rounds+1):
            tmp = tmp[1:] + tmp[:1]
            tmp = bytearray(sbox[i] for i in tmp)
            tmp[0] ^= rcon[i]
            for j in range(self.key_size/4):
                for k in range(4):
                    tmp[k] ^= roundkey[-self.key_size+k]
                roundkey += tmp
        self.roundkey = roundkey

    def get_roundkey(self, k):
        assert k <= self.rounds
        return self.roundkey[self.key_size*k:self.key_size*(k+1)]

    def encrypt(self, plain):
        assert len(plain) == self.key_size
        block = bytearray(plain)
        for i in xrange(self.rounds):
            block = addkey(block, self.get_roundkey(i))
            block = substitute(block)
            if i != self.rounds - 1:
                # Permutation in the last round is of no purpose.
                block = permutation(block)
        block = addkey(block, self.get_roundkey(i+1))
        return block

if __name__ == '__main__':
    from os import urandom
    from struct import pack

    print "Your flag is flag{%s}" % secret.encode('hex')
    f = open('data', 'wb')
    for _ in xrange(8):
        c = zer0TC(secret)
        plaintext = bytearray(urandom(8))
        f.write(pack('8B', *plaintext))
        ciphertext = c.encrypt(plaintext)
        f.write(pack('8B', *ciphertext))
    f.close()
