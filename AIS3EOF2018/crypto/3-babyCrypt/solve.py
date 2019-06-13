#!/usr/bin/python3
import sys
import random

flag = list(b'asdfasdfasdf'.ljust(64, b'\0'))
key = 31337

assert(len(flag) == 64)
random.seed(key)

subs = []
idxs = []
dests = []
nums = []

def makeTable(sub,idx,dest,num) :
    subs.append(sub)
    idxs.append(idx)
    dests.append(dest)
    nums.append(num)

# Save random num
for _ in range(64):
    sub = list(range(256))
    random.shuffle(sub)
    idx = list(range(len(flag)))
    random.shuffle(idx)
    idx = [idx[i:i+2] for i in range(0, len(idx), 2)]
    tmpd = []
    tmpn = []
    for i in range(len(idx)):
        dest = random.sample(idx[:i] + idx[i+1:], len(idx) // 2)
        dest = [k for p in dest for k in p]
        randnum = random.randrange(256)
        tmpd.append(dest)
        tmpn.append(randnum)
    makeTable(sub,idx,tmpd,tmpn)
    

flag = list(b''.fromhex('326dcb14a795600ddc50e4c211f26f9f87730dc2f9e340e9c305ed70f55b4d52f99b9a31d99ef5bdfbac66c455577efce09b1a8774875a688dca260881149dcb'))

for i in range(64):
    sub = subs[::-1][i]
    idx = idxs[::-1][i]
    dest = dests[::-1][i]
    num = nums[::-1][i]
    nxt = flag[:]
    
    for j, (ia, ib) in enumerate(idx): 
        x = sub[flag[ia] ^ flag[ib]]
        x = sub[(x * 13 + 37) & 0xff]
        x = sub[(x + num[j]) & 0xff]
        x = sub[((x >> 3) | (x << 5)) & 0xff]
        for d in dest[j]:
            nxt[d] ^= x

    flag = nxt

print('')
print(bytes(flag))