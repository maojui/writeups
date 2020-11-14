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

bits = [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1]

def int2bits(x):
    return [int(i) for i in f'{x:016b}']

n = len(bits)

def brute(feedback):
    p = []
    for k in range(1 << 16):
        l = LFSR(int2bits(k), int2bits(feedback))
        count = 0
        for i in range(n):
            if l.getbit() == bits[i]:
                count += 1
        if count / n > 0.7:
            print(k, count / n)
            p.append(k)
    return p

p2 = brute(40111)
p3 = brute(52453)

for i1 in range(1 << 16):
    for i2 in p2:
        for i3 in p3:
            l1 = LFSR(int2bits(i1), int2bits(39989))
            l2 = LFSR(int2bits(i2), int2bits(40111))
            l3 = LFSR(int2bits(i3), int2bits(52453))
            for i in range(100):
                x1 = l1.getbit()
                x2 = l2.getbit()
                x3 = l3.getbit()
                x = (x1 & x2) ^ ((not x1) & x3)
                if bits[i] != x:
                    break
            else:
                print(i1.to_bytes(2, 'big') + i2.to_bytes(2, 'big') + i3.to_bytes(2, 'big'))
                break
