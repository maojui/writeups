'''
from : https://gist.github.com/hellman/4950bff09b615e613d46be9eed4bc414

In the challenge we have a "toy block cipher". It is an SPN cipher with:
- 4 rounds
- 8 8-bit S-Boxes (64-bit block)
- bit permutations as linear layer
We are given 2^16 random plaintext/ciphertext pairs.
On contrast with the zer0TC challenge, the bit permutation is strong and provides full diffusion.
The S-Box is weak both differentially and linearly.
Since we have known plaintexts, the way to go is linear cryptanalysis.
We shall attack the first round in order to get the master key and avoid need of key-schedule reversal.
First, we need to find good 3-round linear trails. This can be done using various algorithms/tools.
For example:
Masks after first round: [64,  0, 0, 0, 0, 0, 0,   0],
Masks on ciphertexts:    [242, 0, 0, 0, 0, 0, 242, 0],
Bias: 2^-5.675513
We need to have bias > 2^-8 because we have 2^16 data.
It actually is easier if the bias is around 2^-6,
then the right key byte will be the top candidate in our list with high probability.
The attack procedure:
1. Guess the first key byte (k) of the master key
2. Partially encrypt the first byte of all plaintexts: x' = S(x^k).
3. Compute linear product: c = scalar(x', mask)
4. Compute the bias of all c (i.e. how dis-balanced is the distribution of 0/1).
The right key byte should be in the top candidates sorted by the bias.
After we recover a couple of key bytes,
we can use linear trails which have more active S-Boxes in the first round.
The constraint is only that we have to guess only one extra key byte each time.
Finally, we get the flag: flag{48667ec1a5fb3383}
'''

import math
from zer0SPN import zer0SPN, sbox
sboxinv = map(sbox.index, range(256))

def hw(x):
    if not x: return 0
    return (x & 1) + hw(x >> 1)

scalar = [
    [hw(a & b) & 1 for a in range(256)] for b in range(256)
]



test = True

if test:
    f = open("data",'rb')
    pairs = []
    cipher = open('data','rb').read()
    for i in range( 0, len(cipher),16) :
        pt = [int(p) for p in cipher[i:i+8]]
        ct = [int(c) for c in cipher[i+8:i+16]]

        pairs.append((pt,ct))
        
    TEST_ROUND_KEYS = [[0]*8]*5

else:
    from os import urandom
    key = "abcdefgh"
    c = zer0SPN(key)
    pairs = []
    for _ in range(2**16):
        plaintext = bytearray(urandom(8))
        ciphertext = c.encrypt(plaintext)
        pairs.append((tuple(plaintext), tuple(ciphertext)))
    TEST_ROUND_KEYS = tuple(
        tuple(c.roundkey[i:i+8])
        for i in range(0, len(c.roundkey), 8)
    )

def sl(bias):
    try:
        return "2^%f" % math.log(2, bias)
    except:
        # print(bias
        return "??"

KEY = [None] * 8

# Trails with single-bytes on the plaintext side (after first round)
# To verify correlation we need to guess one key byte
masks = [
    # 1 -5.675513
    [64, 0, 0, 0, 0, 0, 0, 0],
    [242, 0, 0, 0, 0, 0, 242, 0],

    # 2 -5.798370
    [0, 64, 0, 0, 0, 0, 0, 0],
    [138, 0, 0, 0, 0, 0, 138, 0],

    # -7.445192
    # [0, 0, 0, 0, 64, 0, 0, 0],
    # [224, 0, 0, 0, 0, 0, 224, 0],
]
for i in range(0, len(masks), 2):
    inmask, outmask = masks[i:i+2]

    inposes = [i for i in range(8) if inmask[i]]
    outposes = [i for i in range(8) if outmask[i]]

    inpos = inposes[0]
    main_inmask = inmask[inpos]

    results = []
    for k in range(256):
        cor = [0, 0], [0, 0]
        for pt, ct in pairs:
            out = 0
            for i in outposes:
                out ^= scalar[outmask[i]][ct[i]]

            v = pt[inpos]
            v ^= k
            v = sbox[v]
            inp = scalar[main_inmask][v]
            cor[inp][out] += 1

        a, b = cor[0]
        a, b = min(a, b), max(a, b)
        bias = abs(float(a) / (len(pairs)/2.0) - 0.5)
        results.append((bias, k))
    results.sort()

    KEY[inpos] = results[-1][1]
    print("INPOS", inpos, "%02x" % TEST_ROUND_KEYS[0][inpos])
    for bias, k in results[-10:]:
        print("%02x" % k, sl(bias))
    print("KEY", KEY)

print("KEY MID", KEY)

# Trails with multiple bytes on the plaintext side (after first round)
# To verify correlation we need to guess one key byte + use already known
# (order of trails is important)
masks = [
    # 4 -5.482868
    [0, 64, 0, 0, 64, 0, 0, 0],
    [106, 0, 0, 0, 0, 0, 106, 0],

    # 6 -4.754170
    [64, 64, 0, 0, 0, 0, 64, 0],
    [178, 0, 0, 0, 0, 0, 178, 0],

    # 2 -5.653971
    [0, 64, 64, 0, 0, 0, 64, 0],
    [68, 0, 0, 0, 0, 0, 68, 0],

    # 5 -5.745579
    [0, 64, 64, 0, 0, 64, 0, 0],
    [25, 0, 0, 0, 0, 0, 25, 0],

    # 3 -5.725353
    [194, 194, 0, 194, 194, 194, 194, 0],
    [0, 0, 0, 0, 117, 0, 0, 0],

    # 7 -5.353585
    [0, 0, 0, 25, 25, 0, 0, 25],
    [0, 130, 0, 0, 0, 0, 0, 0],
]
for i in range(0, len(masks), 2):
    inmask, outmask = masks[i:i+2]

    inposes = [i for i in range(8) if inmask[i] and KEY[i] is not None]
    outposes = [i for i in range(8) if outmask[i]]

    inpos = [i for i in range(8) if inmask[i] and KEY[i] is None]
    assert len(inpos) == 1
    inpos = inpos[0]
    main_inmask = inmask[inpos]

    results = []
    for k in range(256):
        cor = [0, 0], [0, 0]
        for pt, ct in pairs:
            out = 0
            for i in outposes:
                out ^= scalar[outmask[i]][ct[i]]

            v = pt[inpos]
            v ^= k
            v = sbox[v]
            inp = scalar[main_inmask][v]

            for i in inposes:
                v = pt[i]
                v ^= KEY[i]
                v = sbox[v]
                inp ^= scalar[inmask[i]][v]

            cor[inp][out] += 1

        a, b = cor[0]
        a, b = min(a, b), max(a, b)
        bias = abs(float(a) / (len(pairs)/2.0) - 0.5)
        # print("%02x" % k, cor, sl(bias)
        results.append((bias, k))

    results.sort()

    KEY[inpos] = results[-1][1]
    print("INPOS", inpos, "%02x" % TEST_ROUND_KEYS[0][inpos])
    for bias, k in results[-10:]:
        print("%02x" % k, sl(bias))
    print("KEY", KEY)

print("flag{%s}" % "".join("%02x" % c for c in KEY))

