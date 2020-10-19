#!/usr/bin/env python3
from functools import reduce

class LFSR:
    def __init__(self, init, feedback):
        self.state = init
        self.feedback = feedback
    def getbit(self):
        nextbit = reduce(lambda x, y: x ^ y, [i & j for i, j in zip(self.state, self.feedback)])
        self.state = self.state[1:] + [nextbit]
        return nextbit

class MYLFSR:
    def __init__(self, inits):
        inits = [[int(i) for i in f"{int.from_bytes(init, 'big'):016b}"] for init in inits]
        self.l1 = LFSR(inits[0], [int(i) for i in f'{39989:016b}'])
        self.l2 = LFSR(inits[1], [int(i) for i in f'{40111:016b}'])
        self.l3 = LFSR(inits[2], [int(i) for i in f'{52453:016b}'])
    def getbit(self):
        x1 = self.l1.getbit()
        x2 = self.l2.getbit()
        x3 = self.l3.getbit()
        return (x1 & x2) ^ ((not x1) & x3)
    def getbyte(self):
        b = 0
        for i in range(8):
            b = (b << 1) + self.getbit()
        return bytes([b])

def xor(a, b):
    return bytes([i ^ j for i, j in zip(a, b)])

FLAG = open('./flag', 'rb').read()
assert len(FLAG) == 12
assert FLAG.startswith(b'FLAG{')
assert FLAG.endswith(b'}')
FLAG = FLAG[5:-1]

lfsr = MYLFSR([FLAG[0:2], FLAG[2:4], FLAG[4:6]])
print([lfsr.getbit() for _ in range(100)])
