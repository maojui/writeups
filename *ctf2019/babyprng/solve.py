import hashlib
from pwn import *
from cryptools import B2s


#conn = remote('34.92.185.118', 10002)
conn = remote('localhost',10001)
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

#postfix = conn.recvuntil(') == ')[12:-5]
#val = B2s(conn.recvuntil('\n').strip())
#ans = pow(postfix,val)

#conn.sendline(ans)
conn.recvuntil('opcode(hex): ')
conn.sendline('040102'*20 +'000500050034')
flag = conn.recvuntil('\n')
print(flag)

# *ctf{23bb9d2dc5eebadb04ea0f9cfbc1043f}
conn.close()
