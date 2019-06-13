import hashlib
import os
from pwn import *
from cryptools import *

# conn = remote('34.92.185.118', 10001)
conn = remote('127.0.0.1', 10000)

# avaliable = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

# def pow(postfix, val):
#     for a in avaliable :
#         print(chr(a),end='\n')
#         for b in avaliable :
#             for c in avaliable :
#                 for d in avaliable :
#                     xxxx = bytes([a,b,c,d])
#                     if hashlib.sha256( xxxx + postfix).hexdigest() == val :
#                         return xxxx

# postfix = conn.recvuntil(') == ')[12:-5]
# val = conn.recvuntil('\n').strip().encode()  
# ans = pow(postfix,val)

# conn.sendline(ans)

def bytes2num(b):
    return [int(bb) for bb in b]

def xor(l1,l2):
    return bytes(map(lambda x: x[0]^x[1], zip(l1,l2)))

def encrypt(pt):
    conn.recvuntil('plaintext(hex): ')
    conn.sendline(pt)
    return conn.recvuntil('\n').strip()

def rev(cipher):
    ''' 回到 k3 xor 處 '''
    cipher = bytes.fromhex(cipher)[:8]
    l, r = cipher[:4],cipher[4:]
    l, r = bytes(xor(l,r)), bytes(l)
    return ('0x'+bytes.hex(l),'0x'+bytes.hex(r))

def diff(plain,d):
    return bytes.hex(xor(bytes.fromhex(plain),bytes.fromhex(d)))

def gbox(a,b,mode):
    x = (a+b+mode)%256
    return ((x<<2)|(x>>6))&0xff

def fbox(plain):
    t0 = (plain[2] ^ plain[3])
    y1 = gbox(plain[0] ^ plain[1], t0, 1)
    y0 = gbox(plain[0], y1, 0)
    y2 = gbox(t0, y1, 0)
    y3 = gbox(plain[3], y2, 1)
    return [y3, y2, y1, y0]

plaintxt = []
rounds = []
import time
time.sleep(3)
for i in range(30) :
    plain0  = bytes.hex(os.urandom(8))
    plain1 = diff(plain0,'0000000080800000')
    plain2 = diff(plain0,'8080000080800000')
    plain3 = diff(plain0,'0000000200000000')
    plain4 = diff(diff(plain0,'0000000000000002'),bytes.hex(os.urandom(4)*2))
    
    pts = [plain0,plain1,plain2,plain3,plain4]
    plaintxt.append( [ ('0x'+pt[:8], '0x'+pt[8:]) for pt in pts])

    cipher = encrypt(''.join(pts))
    r3 = list(  (rev(B2s(cipher[16*i:16*(i+1)])) for i in range(5) ) )
    rounds.append(r3)

conn.interactive()
# conn.recvuntil('and your flag:\n')
# flag = conn.recvuntil('\n').strip()


# conn.interactive()
# conn.close()