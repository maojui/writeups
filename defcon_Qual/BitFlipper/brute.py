# coding: utf-8
from hashlib import *
from pwn import *

a = set()
def pow_hash(challenge, solution):
    return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1

cha_set = []
sol_set = []

guess = 0x50


with open('bit_step','a') as f:
    while True:
        r = remote("61421a06.quals2018.oooverflow.io",5566)
        r.recvuntil("Challenge: ")
        challenge = r.recvuntil("\n")[:-1]
        
        # challenge = switchBS(conn.recvuntil('\n').strip())
        # print(challenge)

        r.recvuntil("n: ")
        n = r.recvuntil("\n")
        r.recvuntil("Solution: ")
        #search table
        if (challenge, n) in cha_set:
            solution = sol_set[cha_set.index((challenge,n))]
        else:
            conn2 = remote('140.112.31.111',13377)
            conn2.sendline(str(challenge)+' 22')
            solution = conn2.recv()
            conn2.close()
            cha_set.append((challenge, n))
            sol_set.append(solution)

        r.sendline(str(solution))
        r.recvuntil("How many faults you want to introduce?")
        r.sendline("1")
        r.recvuntil("(")
        lowerBound, upperBound = r.recvuntil(")").split("-")
        r.sendline(str(guess))
        r.recvuntil("ion: ")
        md5 = r.recvuntil("\n")
        r.recvuntil("---\n")
        response = r.recv()
        print("lowerBound: {}, upperBound: {}, guess: {}, md5: {}".format(lowerBound, upperBound, hex(guess),md5))
        print("response :" + response)
        f.write( str(guess) + ',' + response)
        guess += 16
        r.close()
# print cha_set, sol_set
#r.interactive()

