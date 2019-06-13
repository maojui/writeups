from pwn import *
from task import *

def fakeMao192(s, A,B,C,D,E,F,offset):
    mask = 0xFFFFFFFF
    def G(X,Y,Z):
        return (X ^ (~Z | ~Y) ^ Z) & mask
    def H(X,Y,Z):
        return (X ^ Y ^ Z & X) & mask
    def I(X,Y,Z):
        return ((X & ~Z) | (~Z & Y)) & mask
    def J(X,Y,Z):
        return ((X ^ ~Z) | (X & ~Y)) & mask
    def K(X,Y,Z):
        return ((~X & Z) | (~X & Z ^ ~Y)) & mask
    def L(X,Y,Z):
        return ((~X & Y ^ Z) | (X & Y)) & mask
    def M(X,Y):
        return (X << Y | X >> (32 - Y)) & mask
    X = [int((mask-1) * cos(i)) & mask for i in range(256)]
    s_size = len(s)
    s += bytes([0xb0])
    if len(s) % 128 > 120:
        while len(s) % 128 != 0: s += bytes(1)
    while len(s) % 128 < 120: s += bytes(1)
    s += bytes.fromhex(hex( (s_size+offset) * 8)[2:].rjust(16, '0'))
    print(s)
    for i, b in enumerate(s):
        k, l = int(b), (i+offset) & 0x1f
        A = (B + M(A + G(B,C,D) + X[k], l)) & mask
        B = (C + M(B + H(C,D,E) + X[k], l)) & mask
        C = (D + M(C + I(D,E,F) + X[k], l)) & mask
        D = (E + M(D + J(E,F,A) + X[k], l)) & mask
        E = (F + M(E + K(F,A,B) + X[k], l)) & mask
        F = (A + M(F + L(A,B,C) + X[k], l)) & mask
    return ''.join(map(lambda x : hex(x)[2:].rjust(8, '0'), [A, F, C, B, D, E]))

# conn = remote('127.0.0.1',12001)
# username = b'maomao'
# password = b'password'
# conn.recvuntil('Input your username : ')
# conn.sendline(username)
# conn.recvuntil(' set a password : ')
# conn.sendline(password)
# conn.recvuntil('your session ID: ')
# sessionID = conn.recvuntil('\n').strip()
# conn.recvuntil('&&sessionID) : ')
# mac = conn.recvuntil('\n').strip()
# conn.recvuntil('you want to do?\n')

# print(mac)
# print(sessionID)

# def sendcmd(cmd):
#     new_mac = vertify(username,password,sessionID,cmd)
#     conn.sendline(b'&&'.join([new_mac,sessionID,cmd]) )
#     return conn.recvuntil('you want to do?\n')

# print(sendcmd(b'read'))


# conn = remote('127.0.0.1',10205)
conn = remote('maojui.me',11111)
username = b'Admin'
# username = b'maomao'
# password = b'password'
conn.recvuntil('Input your username : ')
conn.sendline(username)
# conn.recvuntil(' set a password : ')
# conn.sendline(password)
conn.recvuntil('your session ID: ')
sessionID = conn.recvuntil('\n').strip()
conn.recvuntil('&&sessionID) : ')
mac = conn.recvuntil('\n').strip()
conn.recvuntil('you want to do?\n')

print(mac)
print(sessionID)

print("START HACK")
extend = b'&&flag'
sp_hash = [int(mac[i*8:i*8+8],16) for i in range(6)]

size = len(username)+2+64+2+len(sessionID)

pad = bytes([0xb0])
if (size+len(pad)) % 128 > 120:
    while (size+len(pad)) % 128 != 0: 
        print((size+len(pad)))
        pad += bytes(1)
while (size+len(pad)) % 128 < 120: 
    pad += bytes(1)

print(pad)
pad += bytes.fromhex(hex( size * 8)[2:].rjust(16, '0'))
new_mac = fakeMao192(extend,sp_hash[0],sp_hash[3],sp_hash[2],sp_hash[4],sp_hash[5],sp_hash[1],size+len(pad)).encode()
print(new_mac)
payload = b'&&'.join([new_mac,sessionID+pad,b'flag'])
print(payload)
conn.sendline(payload)
# print(conn.recvuntil('\n'))
# print(conn.recvuntil('\n'))
print(conn.recvuntil('\n'))
# conn.interactive()