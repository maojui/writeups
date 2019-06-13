#!/usr/bin/python3
import sys
import random
from cryptools import *

# with open('flag.txt', 'rb') as f:
#     flag = f.read().strip()
flag = b'EOF{fuck you EOF }'
flag = list(flag.ljust(64, b'\0'))
print(flag)
key = 31337

flag = list(bytes(n2s(8689349034430455055716439199954966437047934776655610553421809769104737665711135266839688172404890627691801684851363541706587227838657616411782457676094173)[:]))
print(flag)
assert(len(flag) == 64)

random.seed(key)

xor_by = {}
for i in range(64):
    xor_by[i] = []
counter = 0


for _ in range(64):
    sub = list(range(256))
    random.shuffle(sub)
    idx = list(range(len(flag)))
    random.shuffle(idx)
    idx = [idx[i:i+2] for i in range(0, len(idx), 2)]
    nxt = flag[:]
    for i, (ia, ib) in enumerate(idx):
        dest = random.sample(idx[:i] + idx[i+1:], len(idx) // 2)
        dest = [k for p in dest for k in p]
        x = sub[flag[ia] ^ flag[ib]]
        x = sub[(x * 13 + 37) & 0xff]
        x = sub[(x + random.randrange(256)) & 0xff]
        x = sub[((x >> 3) | (x << 5)) & 0xff]
        for d in dest:
            nxt[d] ^= x
            xor_by[d].append(counter)
        counter  += 1
    flag = nxt


flag = bytes(flag).hex()

table = [0] * 2048

def reset():
    table = [0]*2048


def checkTable(checkTable, xorIDX):
    for tmp in xor_by[xorIDX] : 
        checkTable[tmp] ^= 1 


def calCheckTable(checkTable, xorIDX):
    for tmp in xor_by[xorIDX] : 
        checkTable[tmp] ^= 1 
    maximum = 0
    idx = 1000
    for i in range(63) :
        if i == xorIDX :
            continue
        counter = 0
        for xored in range(2048) :
            if checkTable[xored] :
                if xored in xor_by[i] :
                    counter += 1
        if counter > maximum :
            maximum = counter
            idx = i
    print("numbers of check : " + str(sum(table)) + ", ",end='')
    print(str(maximum) + " same with " + str(idx))
    calCheckTable(checkTable,idx)
        


# print('Version:')
# print(sys.version)
# print('')
# print('Flag:')
# flag = bytes(n2s(int(flag,16)))
# print(flag)
# flag = list(flag)
# # print(n2s(int(flag,16)))
