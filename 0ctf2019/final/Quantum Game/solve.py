from pwn import *
import numpy as np

conn = remote('127.0.0.1',13337)

# Stage 1
conn.recvuntil('Your turn:')
conn.recvuntil('\n')
conn.sendline('H 0')
conn.sendline('H 0\nX 0')
print("Stage 1 clear.")

# Stage 2
conn.recvuntil('Your turn:')
conn.recvuntil('\n')
conn.sendline('Y 0')
print("Stage 2 clear.")

# Stage 3
conn.recvuntil('(get ')
num = int(conn.recvuntil(' ').strip())
conn.recvuntil('toss the coin? ')
conn.recvuntil('\n')
conn.sendline(f'RX({np.arcsin(np.sqrt(num / 100000)) * 2}) 0')
print("Stage 3 ...")

conn.interactive()
conn.close()

