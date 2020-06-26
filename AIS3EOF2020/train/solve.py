from pwn import *
from cytro import *

# conn = remote('localhost',30005)
conn = remote('eductf.zoolab.org',20002)
conn.sendline('1')
conn.recvuntil('n = ')
n = int(conn.recvline().strip())
e = 3

conn.recvuntil('ticket = ')
ticket = list(map(s2n,chunk(bytes.fromhex(conn.recvline().strip().decode()),128)))

def sendDecrypt(ticket):
    conn.recvuntil('> ')
    conn.sendline('2')
    conn.recvuntil('ticket = ')
    ticket = ''.join(map(lambda x: hex(x)[2:].rjust(128,'0'),ticket))
    conn.sendline(ticket)
    return conn.recvline()
    
ticket = ticket[3:]
flag = ''
for b in range(14):
    for i in range(256,0, -1):
        cipher = []
        cipher.append(ticket[0] - (s2n('|x'.ljust(16-b,'\x00') + flag) - i * (1<<8)**b ))
        cipher.append(ticket[1])
        res = sendDecrypt(cipher)
        if res.find(b'Wrong') != -1 :
            flag = chr( (ord('|') + i) % 256 ) + flag
            print(flag)
            break

