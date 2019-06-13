#!/usr/bin/python3 -u
from Crypto.Cipher import AES
from Crypto.Util import Counter
from cryptools import *
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

def fix(chunks, invalid):
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
    b = np.random.randint(MAX_PAD)
    b = bytes([c | 1 for c in randstr(b)])
    s = a + b'\0' + s + b'\0' + b
    chunks = addRedundant(s)
    chunks = addCRC(chunks)
    s = b''.join(chunks)
    return aesEnc(s, k)


def decrypt(s, k):
    s = aesDec(s, k)
    chunks = chunk(s, 4 + CHUNKSZ)
    if len(chunks) < 2 or len(chunks[-1]) < 4:
        raise ValueError('Invalid size')
    invalid = checkCRC(chunks)
    if invalid is not None:
        chunks = fix(chunks, invalid)
    s = b''.join(c[4:] for c in chunks[1:])
    start = s.find(b'\0')
    if start == -1:
        raise ValueError('Invalid format')
    end = s.find(b'\0', start + 1)
    if end == -1:
        raise ValueError('Invalid format')
    return s[start+1:end]


def genchal():
    key = randstr(16)
    flag = randstr(16).hex()
    print('[*] Example command:')
    cmd = f'getmd5 {PREFIX}{flag}'
    print(encrypt(cmd.encode('ascii'), key).hex())
    # print(f'flag: {flag}', file=sys.stderr)
    return key, flag


score = 0
def challenge():
    global score
    key, flag = genchal()

    for i in range(MAX_REQ):
        try:
            print('')
            cmd = input('[>] cmd: ')
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
        with open('flag.txt') as f:
            print(f'[+] Attack flag: {f.read().strip()}')
    return score


def checkToken(token):
    req = requests.post('http://10.140.0.19/whitelist', {
        'token': token
    })
    req.raise_for_status()
    res = req.json()
    if res['result'] <= 0:
        raise KeyError('Token not found.')


def submitScore(token, score):
    req = requests.post('http://localhost:8081/submit', {
        'point': score,
        'token': token
    })
    req.raise_for_status()
    exit(0)


def main():
    token = input('[>] Team token: ')
    # checkToken(token)
    try:
        challenge()
    except:
        pass
    # submitScore(token, score)


main()