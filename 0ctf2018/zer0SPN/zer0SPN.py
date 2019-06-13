#!/usr/bin/env python
# coding=utf-8

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

class zer0SPN(object):
    '''0ops Substitution–Permutation Network'''

    def __init__(self, key, key_size=8, rounds=4):
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
    from secret import secret
    from os import urandom
    from struct import pack

    print "Your flag is flag{%s}" % secret.encode('hex')
    f = open('data', 'wb')
    for _ in xrange(65536):
        c = zer0SPN(secret)
        plaintext = bytearray(urandom(8))
        f.write(pack('8B', *plaintext))
        ciphertext = c.encrypt(plaintext)
        f.write(pack('8B', *ciphertext))
    f.close()