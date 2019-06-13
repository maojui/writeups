from pwn import *
from hashlib import *
from cryptools import switchBS
import string
import os
from math import sqrt
from libnum import invmod,gcd,nroot,solve_crt

conn = remote('37.139.9.232', 28399)
conn.recvuntil('Submit a printable string X, such that ')
hash_func = getattr(hashlib,switchBS(conn.recvuntil('(X)')[:-3]))
target = switchBS(conn.recvuntil('\n').strip()[-6:])

i = 0
while True :
    i+=1
    if(i%10000==0):print(i)
    rand_hash = hash_func(str(i).encode()).hexdigest()[-6:]
    if target == rand_hash :
        conn.sendline(str(i))
        break

conn.interactive()

test = 1<<1024
phi = 1
while True :
    conn.sendline('p')
    conn.recvuntil(' a, to phirypt:')
    conn.sendline(str(test))
    conn.recvuntil('(n) =')
    phi = int(conn.recvuntil('\n').strip())
    # print(test,phi)
    if test == phi :
        test *= 2
    else :
        phi = test - phi
        print(phi)
        break

conn.sendline('F')
conn.recvuntil('(flag), e, n) =')
eflag = int(conn.recvuntil('\n').strip())

print('********** get phi **********')
print(phi)
print('********** eflag **********')
print(eflag)


def enc(num):
    conn.sendline('E')
    conn.recvuntil(' m, to encrypt:')
    conn.sendline(str(num))
    conn.recvuntil('e, n) = ')
    return int(conn.recvuntil('\n').strip())

def enc(num):
    return pow(num,1238497123749102734917340134891703947129083741902,n)

print('********** find n **********')
num = []
for _ in range(10):
    r = random.randint(2,100)
    num.append(enc(r)**2 - enc(r**2))

n = gcd(*num)

print(n)

ppqs = (n-phi+1)**2
pmqs = ppqs - 4*n
ppq = (n-phi+1)
pmq = nroot(pmqs,2)
q = (ppq - pmq)//2
p = (ppq + pmq)//2

assert n == p*q
assert phi == (p-1)*(q-1)


conn.interactive()
    
factors = factordb()

cs = []
ns = []
for k,v in factors:
    ns.append(pow(k,v))
    cs.append(1)

solve_crt(ns,cs)
# F = pow(e*flag,e,n)
# x % phi