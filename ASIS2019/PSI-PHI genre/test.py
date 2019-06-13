from libnum import *
from Crypto.Util.number import *

p = getPrime(100)
q = getPrime(100)
n = p*q
e = getPrime(30)
phi = (p-1)*(q-1)
d =invmod(e,(p-1)*(q-1))

m = 1234
a = m
for i in range(1,10000):
    m *= m
    x = pow(m,e,n)
    a = (a*m*x)%n
    if(a < n//1000) :
        print(a)