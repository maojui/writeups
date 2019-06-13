#-*- coding:utf-8 -*-

import sys
import random

from zer0C4 import ksa, prga, N, mask

def prga0(s, n):
    """weakened prga"""
    i = j = 0
    res = bytearray()
    for _ in range(n):
        i = (i + 1) & mask
        j = (j + s[i]) & mask
        # s[i], s[j] = s[j], s[i]
        res.append(s[(s[i]+s[j])&mask])
    return tuple(res)

def randvec():
    return [random.randint(0, 31) for _ in xrange(16)]

secret_key = randvec()

def calc_score(stream, stream0):
    score = 0
    step = 0.2
    wt = 1 + step * 16
    nmatch = 0
    for c0, c in zip(stream0, stream):
        ok = ((c % b) == (c0 % b))

        nmatch += ok
        score += wt * ok
        wt -= step
    return score

q = int(sys.argv[1])
b = 2**q
l = 16

stream0 = None

lst = []
lstbad = []
for i in xrange(16000):
    key = randvec()
    for i in xrange(16):
        key[i] -= key[i] % b
        key[i] += (1 - i) % b
    s = ksa(key)
    if stream0 is None:
        stream0 = prga0(s, 16)

    stream = prga(s, 16)
    score = calc_score(stream, stream0)
    lst.append(score)

    key = randvec()
    for i in xrange(16):
        key[i] -= key[i] % (b/2)
        key[i] += (1 - i) % (b/2)
    s = ksa(key)
    stream = prga(s, 16)
    score = calc_score(stream, stream0)
    lstbad.append(score)

lst.sort()
lstbad.sort()
print "avg", sum(lst) / float(len(lst))
print "avgbad", sum(lstbad) / float(len(lstbad))
print "med", lst[len(lst)/2]
print "medbad", lstbad[len(lstbad)/2]
for x in xrange(30):
    print "%2d" % x, ":",
    print "%5d" % sum(1 for v in lst if v >= x),
    print "%5d" % sum(1 for v in lstbad if v >= x),
    print " | ",
    print "%6.2f%%" % (sum(1 for v in lst if v >= x) / float(len(lst)) * 100),
    print "%6.2f%%" % (sum(1 for v in lstbad if v >= x) / float(len(lstbad)) * 100),
    print
