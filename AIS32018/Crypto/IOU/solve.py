import os
from cryptools import *
from Crypto.Util.number import long_to_bytes
import itertools
from pwn import *

conn = remote('104.199.235.135' ,20002)

#  ...
#  damn Prove of Work
#  ...

conn.recvuntil('m =')
m = int(conn.recvuntil('\n').strip())
conn.recvuntil('s =')
s = int(conn.recvuntil('\n').strip())
conn.recvuntil('n =')
n = int(conn.recvuntil('\n').strip())
conn.recvuntil('e =')
e = int(conn.recvuntil('\n').strip())

print("[+] GET : ",m,s,n,e)

while True :
    signature = os.urandom(2048//10)
    temp = pow(s2n(signature),e,n)
    temp = long_to_bytes(temp)
    try :
        if int(temp.split()[3]) > 10 :
            break
    except :
        pass

print("[+] Fake Signature with {} bucks.".format(int(temp.split()[3])))

signature = s2n(signature)
m = pow(signature,e,n)

conn.sendline(str(m))
conn.sendline(str(signature))

while True :
    try :
        message = conn.recv()
        if 'AIS3' in message :
            print(message)
    else :
        break

