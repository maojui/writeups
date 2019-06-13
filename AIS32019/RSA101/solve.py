from pwn import *
from cytro import invmod,n2s

conn = remote('35.221.138.171', 10201)
conn.recvuntil(' : (')
e = int(conn.recvuntil(',')[:-1].strip())
n = int(conn.recvuntil(')')[:-1].strip())

conn.recvuntil('Encrypted Flag : ')
flag = int(conn.recvuntil('\n').strip())

def test_num(num):
    conn.recvuntil('n = ? \n')
    conn.sendline( str(num) )
    conn.recvuntil('(n % phi) % 64 = ')
    return int(conn.recvuntil('\n').strip())

phi = 0
rem = 0

for i in range(2049, 5, -1):
    res = test_num((1 << i) + phi)
    print(res)
    if res == 0:
        phi |= (1 << i)
    else :
        if i < 1000  and rem == 0 :
            rem = res

print(phi)
phi += (64 - rem)
print(phi)
print( n2s(pow(flag,invmod(e,phi),n) ))