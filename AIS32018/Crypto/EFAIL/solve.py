from pwn import *
from cryptools import *
from cryptools.CBC import CBC_XOR
import string
import random

conn = remote('104.199.235.135' ,20003)

#  ...
#  damn Prove of Work
#  ...

conn.recvuntil('> ')
conn.sendline(b'1')
cipher = conn.recvuntil('\n')
print('Get cipher : ',cipher)

b64cipher = cipher.strip()
cipher = switchBS(b64d(b64cipher))


temp = CBC_XOR(cipher[256-16:256] ,"'\n\n--BOUNDARY\nTy", "\'\nweb\'d.djo6.ml/")
temp2 = xor_string(cipher[448:512],"kbcd")
temp3 = CBC_XOR(cipher[512-16:512] ,"\nType: text\nHope","\'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

cipher = cipher[:256]+ temp + cipher[256:256+16] + temp2 + cipher[448+4:512] + temp3 + cipher[512:]

payload = b64e(switchBS(cipher))

conn.recvuntil('> ')
conn.sendline(b'2')
conn.sendline(payload)

conn.interactive()


