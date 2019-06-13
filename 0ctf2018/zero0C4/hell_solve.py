#-*- coding:utf-8 -*-

"""
In this challenge we have a weakened version of RC4.
It operations on permutation of values 0..31.
Moreover, i is incremented in the beginning of the loop instead of the end.
We are given access to a related-key oracle.
We can send any key delta and the server will return us the generated sequence using the key xored with our delta.
There is a well known paper
"Weaknesses in the Key Scheduling Algorithm of RC4."
by Fluhrer, Mantin, Shamir.
In Section 8 they describe a Related Key attack.
And it actually works better if the key schedule is modified exactly as in the challenge.
The main idea is that we can recover the 16-byte key in layer of 16 bits, from LSBs of each key byte to MSBs.
If LSBits of the key bytes form a special pattern, then the LSBits of the output sequence correlate with a special sequence.
The script stat.py can be used to choose correlation bound for filtering wrong keys.
It is slightly difficult because we have only 1500 queries of 512 deltas, that is 2^19.5 deltas total.
We can recover 4 LSBits of each key byte and then bruteforce the 16 MSBits locally.
With a good probability we get the key.
The flag: flag{Haha~~Do_y0u_3nj0y_ouR_stre4m_c1pher?}
"""

import string
import random
from hashlib import sha256
from struct import pack
from itertools import product
from hashlib import sha256

from sock import Sock

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

def bconserves_t(b, s, t):
    return s[t] % b == t % b

def bconserving(b, s):
    num = 0
    for t in xrange(len(s)):
        num += bconserves_t(b, s, t)
    return num == len(s)

def bexact(b, key):
    for t in xrange(16):
        if key[t] % b != (1 - t) % b:
            return False
    return True

def randvec():
    return [random.randint(0, 31) for _ in xrange(16)]

f = Sock("202.120.7.220 1234")

# pow
# sha256(XXXX+JyZoJLkhS8Jhsoxi) == 6387c59e693c59880ff6458c048a089aac925573cd27d61dcce6e4049dac084d
# Give me XXXX:
alpha = string.ascii_letters + string.digits
suff, target = f.read_until_re(r"XXXX\+(\w+)\) == (\w{64})").groups()
print suff, target
for p in product(alpha, repeat=4):
    p = "".join(p)
    if sha256(p + suff).hexdigest() == target:
        break
else:
    print "FAIL"
    quit()
print p
f.send(p)
print "ok"


lastdelta = [0] * 16
NQ = 0
NQALL = 0

def oracle_chunk(deltas):
    global NQ, NQALL, lastdelta
    res = []
    NQ += 1
    NQALL += 1
    f.read_until("2. Guess the key.\n")
    f.send("1\n")

    s = ""
    for delta in deltas:
        tosave = delta[::]
        delta = delta[::]
        for i in xrange(16):
            s += chr(delta[i] ^ lastdelta[i])
        lastdelta = tosave
    f.send(pack("H", len(s)))
    f.send(s)
    f.read_until("Here is you xor-key: ")
    res = map(ord, f.read_nbytes(len(s)))
    for c in res: assert 0 <= c < 32
    return [res[i:i+16] for i in xrange(0, len(res), 16)]

def calc_score(stream):
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


bits16 = tuple(product(range(2), repeat=16))

def genchunk(offsets):
    alldeltas = []
    for offset in offsets:
        bits = bits16[offset]
        delta = randvec()
        for i in xrange(16):
            delta[i] -= delta[i] % b
            delta[i] += known_delta[i] % (b/2)
            delta[i] += bits[i] << (q - 1)
        alldeltas.append(delta)
    return alldeltas

def getavg(off):
    return data[off][0] / float(data[off][1])

def add_scores():
    all_offs = list(offs)
    for i in xrange(0, len(all_offs), 512):
        cur_offs = all_offs[i:i+512]
        while len(cur_offs) + len(all_offs[i:i+512]) <= 512:
            cur_offs += all_offs[i:i+512]

        chunk = genchunk(cur_offs)
        outs = oracle_chunk(chunk)

        for off, out in zip(cur_offs, outs):
            score, num = data[off]
            score += calc_score(out)
            num += 1
            data[off] = score, num

# q = 1
# 25 : 13023 81.39375 % good
# 25 : 3992 24.95 % bad

# avg: 21.9 vs 29.6
# 20 : 15396 96.225 %
# 20 : 10481 65.50625 %

known_delta = [0] * 16

for q in xrange(1, 5):
    NQ = 0
    b = 2**q

    testkey = randvec()
    for i in xrange(16):
        testkey[i] -= testkey[i] % b
        testkey[i] += (1 - i) % b
    s = ksa(testkey)
    stream0 = prga0(s, 16)
    assert bexact(b, testkey)
    assert bconserving(b, s)

    offs = set(range(2**16))
    data = {i: (0, 0) for i in offs}

    bounds = None
    if q == 1: bounds = [23, 23, 24, 25, 25, 25, 25, 25, 25, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 26]
    if q == 2: bounds = [13, 14, 17, 17, 19] + [19] * 100
    if q == 3: bounds = [8, 9, 10, 12, 14, 16] + [17] * 100
    if q == 4: bounds = [8, 8, 9, 10, 11] + [12] * 100
    if bounds is None: break

    for bound in bounds:
        add_scores()
        offs = filter(lambda off: getavg(off) >= bound, offs)
        print len(offs), "nq", NQ, "total", NQALL
        if len(offs) <= 1:
            break

    assert len(offs) == 1, "fail"
    ans = bits16[offs.pop()]
    bitmask = 1 << (q - 1)
    for i in xrange(16):
        known_delta[i] |= ans[i] << (q - 1)

    print "known_delta", known_delta, "after", "q =", q

def test_key(key):
    for delta, out in zip(deltas, outs):
        test = [x^y for x, y in zip(key, delta)]
        s = ksa(test)
        stream = prga(s, 16)
        if tuple(stream) != tuple(out):
            break
        return True

deltas = [randvec() for _ in xrange(512)]
outs = oracle_chunk(deltas)

b = 2**4
key = [0] * 16
for i in xrange(16):
    key[i] += (1 - i) % b
    key[i] ^= known_delta[i]

print "KEY PART", key
print "SEED", seed

for bits in bits16:
    for i in xrange(16):
        key[i] ^= key[i] & (1 << 4)
        key[i] ^= bits[i] << 4

    if test_key(key):
        print "WIN", key
        break
else:
    print 'no match..'

f.read_until("2. Guess the key.\n")
f.send("2\n")

k = "".join(map(chr, key))
f.send(k)

f.interact()