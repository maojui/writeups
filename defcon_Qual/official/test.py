from pwn import *
import sys
import struct
import hashlib
from cryptools import *
# inspired by C3CTF's POW

def pow_hash(challenge, solution):
    return hashlib.sha256(challenge + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1

conn = remote('3aef2bbc.quals2018.oooverflow.io',31337)
conn2 = remote('140.112.31.111',13377)
print(conn.recvuntil('Challenge: '))
challenge = switchBS(conn.recvuntil('\n').strip())
# print(challenge)
conn2.sendline(f'{challenge} 22')
ans = switchBS(conn2.recv())
conn2.close()

print(ans)
conn.sendline(str(ans))
conn.interactive()

def hash(x):
    return int(sha1(x).hexdigest(),16)

((pow(g,(hash(b'cat')%q),p)*pow(y,r,p))%p)%q
# print(conn.recv())

# def flip(n):
#     conn.sendline(str(n))
#     print(conn.recv())


# test = 2
# flip(test)


# # flip(50000)
# flip(30000)
# flip(20000)
# # flip(40000)

# while True :
#     print(conn.recvuntil('\n'))

