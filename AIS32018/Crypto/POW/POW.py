from pwn import *
from cryptools import *
import itertools
import string
import random

pass_pow = False
while not(pass_pow):
    conn = remote('104.199.235.135', 20000)
    conn.recvuntil("x[:6] == '")
    start = conn.recvuntil("'").strip(b'\'')
    conn.recvuntil('\n')
    print(start)
    conn.recvuntil('x = ')
    i = 0
    count = 0 
    for c in itertools.product(string.digits + string.ascii_letters, repeat=6):
        count += 1
        tail_str = switchBS(''.join(c))
        if hashlib.sha256(start + tail_str).hexdigest().startswith('000000'):
            print("find ... ")
            pass_pow = True
            conn.sendline(start + tail_str)
            break
        if count % 100000 == 0 : print(count)
        if count > 50000000:
            conn.close()
            break

# conn.sendline(x)
conn.interactive()