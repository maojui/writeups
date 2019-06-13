from pwn import *
import sys
import struct
import hashlib

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

conn = remote('61421a06.quals2018.oooverflow.io',5566)
conn.recvuntil('Challenge: ')
challenge = conn.recvuntil('\n').strip()
n = int(conn.recvuntil('\n').strip().split()[-1])

ans = solve_pow(challenge,n)
conn.sendline(str(ans))

print(conn.recv())

def flip(n):
    conn.sendline(str(n))
    print(conn.recv())

conn.interactive()

# test = 2
# flip(test)


# # flip(50000)
# flip(30000)
# flip(20000)
# # flip(40000)

# while True :
#     print(conn.recvuntil('\n'))

