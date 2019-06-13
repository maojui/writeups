
# Hard RSA

The most problem is e = 2 

This means invmod(e,phi), phi is (prime-1)*(prime-1)

So that, gcd(e,prime-1) => 2

My solve is calculate, sqrt(c) in p,q respectively, and CRT them to recover module number.

```python
from Crypto.PublicKey import RSA
from cryptools import *

pub = RSA.importKey(open('pubkey.pem','r').read())
n = pub.n
e = pub.e
p = 275127860351348928173285174381581152299
q = pub.n//p
assert n == p*q
phi = (p-1)*(q-1)

flag = s2n(open('flag.enc','rb').read())
r1 = list(sqrtmod_prime_power(flag,p,1))
r2 = list(sqrtmod_prime_power(flag,q,1))
for a in r1 :
    for b in r2 :
        print(n2s(solve_crt([a,b],[p,q])))
```

### Flag : PCTF{sp3ci4l_rsa}