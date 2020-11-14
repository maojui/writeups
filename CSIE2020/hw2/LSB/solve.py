from pwn import *
from libnum import *

e = 65537

conn = remote('140.112.31.97', 30001)
conn.recvuntil(' = ')
n = int(conn.recvline().strip())

conn.recvuntil(' = ')
c = int(conn.recvline().strip())

def guess(num):
    conn.sendline(str(num))
    conn.recvuntil('m % 3 = ')
    ob = int(conn.recvline().strip())
    return ob

oracle = 3

upper_bound = n
lower_bound = 0

mult = pow(oracle, e, n)
for count in range(0, int(math.log(n, oracle))+1 ):
    c = (mult * c) % n
    bits_val = guess(c)
    for i in range(oracle) :
        if bits_val == (-n * i) % oracle :
            diff = upper_bound - lower_bound 
            upper_bound = lower_bound + (diff * (i + 1) // 3 ) + 1
            lower_bound = lower_bound + (diff * i // 3)
            break
    print(f'bound: {lower_bound} ~ {upper_bound})')

    if lower_bound+1 == upper_bound :
        break

for flag in range(lower_bound, upper_bound) :
    print(n2s(flag)[-26:])