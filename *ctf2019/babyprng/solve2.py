import hashlib
from pwn import *
from cryptools import B2s


conn = remote('34.92.185.118', 10003)
# conn = remote('127.0.0.1', 10004)

avaliable = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def pow(postfix, val):
    for a in avaliable :
        print(chr(a),end='\n')
        for b in avaliable :
            for c in avaliable :
                for d in avaliable :
                    xxxx = bytes([a,b,c,d])
                    if hashlib.sha256( xxxx + postfix).hexdigest() == val :
                        return xxxx

postfix = conn.recvuntil(') == ')[12:-5]
val = B2s(conn.recvuntil('\n').strip())
ans = pow(postfix,val)

conn.sendline(ans)
conn.recvuntil('opcode(hex): ')
conn.sendline('0301060134'+ '0304000039')
flag = conn.recvuntil('\n')
print(flag)
# *ctf{e48af588d4b80ade5ad44a8b5c90d222}

conn.close()
