from pwn import *
import math

conn = remote('39.96.8.114',9999)
for i in range(10):
    print(conn.recv())
    conn.sendline(str(2**120))
    print(conn.recvuntil('This is the sum:'))
    a = int(conn.recvuntil('\n').strip())
    a = bin(a)[2:]
    n = 120
    listNum = [a[-i-n:-i] for i in range(0,len(a),n) ][1:][::-1] + [a[-n:]] 
    response = ' '.join(map(lambda x:str(int(x,2)),listNum))
    conn.sendline(response)
    
conn.interactive()
# BCTF{One_T1m3_10_Gue33_Coeff_1s_0K!}