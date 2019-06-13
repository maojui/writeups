import math
from cryptools import *
from zlib import crc32

def chunk(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

def addCRC(chunks):
    return [crc32(c).to_bytes(4, 'big') + c for c in chunks]

tmp = b'\x00getmd5 31337313373133731337313373133731cc61e7186846286e8b7b45364b4efcd6\x00'

whitelist = set(tmp)

def test(start):
    a = b''.join(addCRC( chunk( b'\xaa'*start + tmp , 32) ))
    a += b'\xaa' * (16 - (len(a) % 16))
    a = chunk(a ,16)
    return a

testList = []
for i in range(32):
    testList.append(test(i))

for i in range(32):
    print(i)
    tmpC = testList[i]
    subarray = [c[-1] in whitelist  for c in tmpC]
    subword = [ chr(c[-1]) for c in tmpC ]
    trueLine = {}
    for i in range(len(subarray)-1) :
        if subarray[i] == True :
            trueLine[i] = subarray[i+1:].index(False) + 1
        else :
            trueLine[i] = 0
    blockIDX = max(trueLine.items(), key=operator.itemgetter(1))[0]
    while True :
        if not subword[blockIDX].isdigit() :
            if subword[blockIDX] in '\x00getmd5 ':
                break
            blockIDX += 1
        else :
            break

    result = tmpC[blockIDX+5]

    if not b'\x00' in result :
        if sum([i in whitelist for i in result[-4:]]) == 0 :
            result = tmpC[blockIDX+6]
            if not b'\x00' in result :
                print(result)
                print(subword)
                print()
                print(subarray)


b'\x1e\xc3\x9b\xc3\xa6C\xc3\xab\xc3\x94\x14\xc2\x80\xc3\xb3\xc2\xbcm^\xc3\xa7\x14\xc2\x98?I\xc3\x9f-\xc3\xa1\xc2\xb8\xc2\x83\xc2\x97\xc2\x82$\xc3\xbf\x15\xc3\x92\xc3\xb2\xc3\xb9\xc2\xae\xc2\x97\xc2\x9f\xc2\xb9H\xc2\x90T$"0\x1f\xc3\x91\x1d]\xc2\xbb\'\xc3\x93\xc3\xa7\x03\xc3\x87)c1\xc3\xbf\xc3\xaf?A\xc3\xa3\xc3\xb1\x7fu7\xc3\x87\xc2\xab\xc2\x87\xc3\xab\xc3\xb1\x17))\xc3\xa5\x15\xc3\xbf\xc3\xa6\xc2\xb6k\xc2\x83s\xc3\x8b\'\x1dws\x07\xc3\x97qE\xc3\x85\xc2\x85\xc2\xaf\xc2\xaf]\'\xc2\x93\xc2\x85Y]\xc2\x97\xc2\x83\xc2\xa3\xc3\x99\xc3\x81\xc2\xa9\x7fO\xc3\xaf\xc3\xads\xc2\x8d\xc2\x8a\xc3\x92\xc2\xad\xc2\x9d\xc3\xaf\xc3\xbd7Qwa\xc3\xab\x01\xc2\x83\xc3\xb15\xc3\x95\xc3\xa1\xc2\x91\xc2\xa5#\xc2\xb3\x00getmd5 313373\xc2\xa9\xc3\xbd\xc3\x83\xc3\xb0133731337313373133731337318bfb75\xc3\xbeC>\r\nc6b678c6abbca31c29d2d47be5\x00\xc3\x85_Q\xc2\x99Y3\xc3\xbd\xc2\x86\xc2\xb3\xc2\x87E\xc2\x9f\xc3\xbb\xc3\x85\xc2\xa3\xc2\x875c\xc2\x93\xc3\xb7\xc3\xbf\xc2\xb9\xc3\x85\xc2\xa7+i\xc2\x99\x7f\xc3\xab\xc2\xb5yU\xc3\xa3\xc3\xa1\xc3\x95M{\xc3\xb1I\xc3\x9f\'q\xc3\xbbxK\xc2\xbbK\xc3\x93]\xc2\xb5#\xc3\x8f+C\t\x7f\xc3\x8f\xc3\x9fc\xc2\x99\x1f\xc3\xafO\xc3\x99\xc3\xaf[\xc3\x9fu\t\t\t\t\t\t\t\t\t\r\n'