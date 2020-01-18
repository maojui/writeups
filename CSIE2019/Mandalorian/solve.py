from pwn import *
from cytro import *
from cytro.asym.rsa import *

conn = remote('edu-ctf.csie.org', 10192)
conn.recvuntil('> ')
conn.sendline('1')
conn.recvuntil('c = ')
c = int(conn.recvline().strip())
e = 65537
conn.recvuntil('n = ')
n = int(conn.recvline().strip())

class Exploit(LSBOracle) :

    def updateConn(self,conn):
        self.conn = conn

    def oracle(self,n) :
        self.conn.recvuntil('> ')
        self.conn.sendline('2')
        self.conn.sendline(str(n))
        self.conn.recvuntil('m = ')
        return int(self.conn.recvline().strip())

exploit = Exploit(n,c,e,4)
exploit.updateConn(conn)
exploit.start()

print(n2s(exploit.get_bound()[0]))
