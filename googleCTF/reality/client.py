from pwn import *
from cytro import *
from decimal import getcontext,Decimal

res = {}
getcontext().prec = 460

# while True :
conn = remote('reality.ctfcompetition.com', 1337)

conn.recvuntil('encrypted flag: ')
flag = conn.recvuntil('\n').strip()
conn.recvuntil(": ")
x1,y1 = [Decimal(num[2:-1]) for num in map(str,conn.recvuntil("\n").strip().split(b', '))]
conn.recvuntil(": ")
x2,y2 = [Decimal(num[2:-1]) for num in map(str,conn.recvuntil("\n").strip().split(b', '))]
conn.recvuntil(": ")
x3,y3 = [Decimal(num[2:-1]) for num in map(str,conn.recvuntil("\n").strip().split(b', '))]

# if res.get(flag[:10],None):
#     print([('whole',flag),(x1,y1),(x2,y2),(x3,y3)])
#     print(res[flag[:10]])
#     break
# else :
#     res[flag[:10]] =  [('whole',flag),(x1,y1),(x2,y2),(x3,y3)]
bignum = pow(2,53)
print( int( bignum / x1) )
print( int( bignum / x2) )
print( int( bignum / x3) )
print(bignum)