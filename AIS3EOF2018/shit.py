#!/usr/bin/python3 -u
from Crypto.Cipher import AES
from Crypto.Util import Counter
from zlib import crc32
import itertools
import numpy as np
import hashlib
import sys
import requests

MAX_REQ = 20000
MAX_PAD = 128
CHUNKSZ = 32
PREFIX = ('31337' * CHUNKSZ)[:CHUNKSZ]
PREFIX = '31337313373133731337313373133731'

def chunk(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

def randstr(n):
    res = np.random.bytes(n)
    return res


def addRedundant(plain):
    chunks = chunk(plain, CHUNKSZ)
    redundant = itertools.zip_longest(*chunks, fillvalue=0)
    redundant = bytes([-sum(z) % 256 for z in redundant])
    return [redundant] + chunks

def addCRC(chunks):
    return [crc32(c).to_bytes(4, 'big') + c for c in chunks]

def pad(plain):
    p = 16 - len(plain) % 16
    return plain + bytes([p]) * p

def unpad(plain):
    if not len(plain) or len(plain) % 16:
        raise ValueError('Invalid padding')
    p = plain[-1]
    if p > 16 or p < 1:
        raise ValueError('Invalid padding')
    if any(c != p for c in plain[-p:]):
        raise ValueError('Invalid padding')
    return plain[:-p]

def aesEnc(s, k):
    s = pad(s)
    ctr = Counter.new(128)
    aes = AES.new(k, AES.MODE_CTR, counter=ctr)
    print("padding : " + str(s[-1]))
    for cc in chunk(s,4+32):
        print(cc)
    print()
    for cc in chunk(s,32):
        print(cc)
    print()
    return aes.encrypt(s)

    
def aesDec(s, k):
    if not len(s) or len(s) % 16:
        raise ValueError('Invalid AES size')
    ctr = Counter.new(128)
    aes = AES.new(k, AES.MODE_CTR, counter=ctr)
    s = aes.decrypt(s)
    return unpad(s)


def checkCRC(chunks):
    invalid = None
    for i, c in enumerate(chunks):
        if c[:4] != crc32(c[4:]).to_bytes(4, 'big'):
            if invalid is not None:
                raise ValueError('Corrupt data')
            invalid = i
    return invalid


others = []
tmp = []
def fix(chunks, invalid):
    global others
    global tmp 
    tmp = chunks
    others = chunks[:invalid] + chunks[invalid+1:] + [[0] * CHUNKSZ]
    recover = itertools.zip_longest(*others, fillvalue=0)
    recover = bytes([-sum(z) % 256 for z in recover])
    recover = recover[4:len(chunks[invalid])]
    crc = chunks[invalid][:4]
    if crc != crc32(recover).to_bytes(4, 'big'):
        raise ValueError('Corrupt data')
    return chunks[:invalid] + [crc + recover] + chunks[invalid+1:]


def encrypt(s, k):
    a = np.random.randint(MAX_PAD)
    a = bytes([c | 1 for c in randstr(a)])
    print("A prefix : " + str(len(a)))
    print(a)
    print()
    b = np.random.randint(MAX_PAD)
    b = bytes([c | 1 for c in randstr(b)])
    print("B prefix : " + str(len(b)))
    print(b)
    print()
    s = a + b'\0' + s + b'\0' + b
    chunks = addRedundant(s)
    print("Redundant : " + str(len(chunks[0])))
    print(chunks[0])
    print()
    chunks = addCRC(chunks)
    
    s = b''.join(chunks)
    return aesEnc(s, k)

def decrypt(s, k):
    s = aesDec(s, k)
    print("Decrypt : ")
    print(s)
    chunks = chunk(s, 4 + CHUNKSZ)
    if len(chunks) < 2 or len(chunks[-1]) < 4:
        raise ValueError('Invalid size')
    invalid = checkCRC(chunks)
    if invalid is not None:
        chunks = fix(chunks, invalid)
        print("FIXED!!!")
    s = b''.join(c[4:] for c in chunks[1:])
    start = s.find(b'\0')
    if start == -1:
        raise ValueError('Invalid format')
    end = s.find(b'\0', start + 1)
    if end == -1:
        raise ValueError('Invalid format')
    return s[start+1:end]

example = ''

def genchal():
    # global example
    key = randstr(16)
    flag = randstr(16).hex()
    print('[*] Example command:')
    cmd = f'getmd5 {PREFIX}{flag}'
    global example
    example = encrypt(cmd.encode('ascii'), key).hex()
    # print(example)
    # print(f'flag: {flag}', file=sys.stderr)
    # print(f'flag: {flag}', file=sys.stderr)
    return key, flag


score = 0
def challenge():
    global score
    key, flag = genchal()
    print()
    for i in range(0,len(example),64) :
        print(example[i:i+64])
    print()
    print(example)
    for i in range(MAX_REQ):
        
        cmd = input('[>] cmd: ')
        # cmd = example
        try:
            print('')
            if cmd.startswith('submit '):
                if cmd[7:] == flag:
                    print('[+] OK')
                    score += 1
                    key, flag = genchal()
                else:
                    print('[!] Wrong')
                    break
            elif cmd.startswith('exit'):
                break
            else:
                cmd = decrypt(bytes.fromhex(cmd), key)
                print(cmd)
                if cmd.startswith(b'getmd5 '):
                    print(f'[+] MD5: {hashlib.md5(cmd[7:]).hexdigest()[:6]}')
                elif cmd.startswith(b'getcrc32 '):
                    print(f'[+] CRC: {crc32(cmd[9:])}')
                else:
                    print(f'[!] Invalid command')
        except ValueError as e:
            print(f'[!] Error: {e}')
        except EOFError:
            return score

    print('')
    print(f'[+] Score: {score}')
    if score > 0:
        print("FLAG!!!!!!")
        # with open('flag.txt') as f:
        #     print(f'[+] Attack flag: {f.read().strip()}')
    return score


# def checkToken(token):
#     req = requests.post('http://10.140.0.19/whitelist', {
#         'token': token
#     })
#     req.raise_for_status()
#     res = req.json()
#     if res['result'] <= 0:
#         raise KeyError('Token not found.')


# def submitScore(token, score):
#     req = requests.post('http://localhost:8081/submit', {
#         'point': score,
#         'token': token
#     })
#     req.raise_for_status()
#     exit(0)


def main():
    # token = input('[>] Team token: ')
    # checkToken(token)
    # try:
    challenge()
    # except:
        # pass
    # submitScore(token, score)


main()

def xor(string, index, ascii) :
    if index < 0 :
        index = index % len(string)
    return string[:index] + bytes([string[index] ^ ascii]) + string[index+1:]

"""
A prefix : 37
b'\xb7\x1b/\xb7!\xa7\x85\x03=K\xf33\xd3\xc7\xb9-\xcd#\xfd\x95\x1f\xa9;\xcf\xfb1Y\x91\x87\xef\xc5\x1fm\x8b\xb7{\x89'

B prefix : 21
b'{\xd9\x8f\xa5\x0f\x1bg\x97\xb5\xb1\x1f\xf3#\xa37E\xd3Mk\x15['

Redundant : 32
b'\x08\xdc(h\xf0\xef\xab.\xe5\xb3?\xffw\xd3b\x93\x0e\xcc\x8a\xeb\x17[w\x17\x84F\x1ba\xdbb\xd3\xfe'

padding : 5
b'\x95\xe6\xf2\xe4\x08\xdc(h\xf0\xef\xab.\xe5\xb3?\xffw\xd3b\x93\x0e\xcc\x8a\xeb\x17[w\x17\x84F\x1ba\xdbb\xd3\xfe'
b'{\xc1*\xda\xb7\x1b/\xb7!\xa7\x85\x03=K\xf33\xd3\xc7\xb9-\xcd#\xfd\x95\x1f\xa9;\xcf\xfb1Y\x91\x87\xef\xc5\x1f'
b'\x00d\xfaJm\x8b\xb7{\x89\x00getmd5 3133731337313373133'
b'\x8e\x11\x12"7313373133731394c57402b61c6449bc'
b'y\xe7\xc4T26f333697b3fe\x00{\xd9\x8f\xa5\x0f\x1bg\x97\xb5\xb1\x1f\xf3#\xa37E\xd3M'
b'p\xcf\x93\xbbk\x15[\x05\x05\x05\x05\x05'

b'\x95\xe6\xf2\xe4\x08\xdc(h\xf0\xef\xab.\xe5\xb3?\xffw\xd3b\x93\x0e\xcc\x8a\xeb\x17[w\x17\x84F\x1ba'
b'\xdbb\xd3\xfe{\xc1*\xda\xb7\x1b/\xb7!\xa7\x85\x03=K\xf33\xd3\xc7\xb9-\xcd#\xfd\x95\x1f\xa9;\xcf'
b'\xfb1Y\x91\x87\xef\xc5\x1f\x00d\xfaJm\x8b\xb7{\x89\x00getmd5 3133731'
b'337313373133\x8e\x11\x12"7313373133731394'
b'c57402b61c6449bcy\xe7\xc4T26f333697b3f'
b'e\x00{\xd9\x8f\xa5\x0f\x1bg\x97\xb5\xb1\x1f\xf3#\xa37E\xd3Mp\xcf\x93\xbbk\x15[\x05\x05\x05\x05\x05'


b6c06afb8fd3b92d1a03f8b04bd79ac1760c2fd74ac356cfddcc0474802f2f00
67b3a4c4a3aa37ad7f17d4ec33347e417538e6edd992a33cea0967190d1020ec
a2bf97733db8f390f3985fef086553a14e8b7c04875492ec0d593959f509a213
bcf761eb578101962a893a6e82ab216ba3785ce2558970138868911b065d298f
4ebab27e1711075f2434861a55227683057502468e28772155ec4986c097513c
234924b79c9aea66a9ce3c1e8546a0e5c475060099717e462312a98f43bb17ff

b6c06afb8fd3b92d1a03f8b04bd79ac1760c2fd74ac356cfddcc0474802f2f0067b3a4c4a3aa37ad7f17d4ec33347e417538e6edd992a33cea0967190d1020eca2bf97733db8f390f3985fef086553a14e8b7c04875492ec0d593959f509a213bcf761eb578101962a893a6e82ab216ba3785ce2558970138868911b065d298f4ebab27e1711075f2434861a55227683057502468e28772155ec4986c097513c234924b79c9aea66a9ce3c1e8546a0e5c475060099717e462312a98f43bb17ff
"""

