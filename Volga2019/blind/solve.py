from pwn import *
from libnum import *
import base64 

conn = remote('blind.q.2019.volgactf.ru', 7070)
print(conn.recvuntil('Enter your command:\r\n'))

cmd = 'cat private_key.py ' 

cmd1 = 51421*140443
cmd2 = 5*239756696507554746480785940207371

m1 = base64.b64encode(n2s(cmd1))
m2 = base64.b64encode(n2s(cmd2))

print(m1)
print(m2)

conn.sendline(f'sig sign')
print(conn.recvuntil('Enter your command to sign:\r\n'))
conn.sendline(m1)
c1 = conn.recvuntil('\n').strip()

conn.sendline(f'sig sign')
print(conn.recvuntil('Enter your command to sign:\r\n'))
conn.sendline(m2)
c2 = conn.recvuntil('\n').strip()

sig = int(c1)*int(c2)



conn.sendline(f'{sig} {cmd}')

conn.interactive()