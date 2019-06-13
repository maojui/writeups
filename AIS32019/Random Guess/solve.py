from pwn import *
from cytro.lcg import *

conn = remote('35.221.138.171',10200)
conn.recvuntil('\n')
conn.recvuntil('\n')
conn.recvuntil('N = ')
nums = list(map(int,conn.recvuntil(b'\n').strip().split(b', ')))

a,b,n = find_modulus(nums)
lcg = LCG(nums[-1],a,b,n)
for _ in range(100):
    states = lcg.next()
    print(states)
    conn.sendline(str(states))
    conn.recvuntil('Good!\n')
    
conn.interactive()