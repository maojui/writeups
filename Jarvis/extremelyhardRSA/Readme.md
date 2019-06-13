# Extremely Hard RSA

I bet this is not too big LoL. Fortunately, finish at `118719488`.

```python
from Crypto.PublicKey import RSA
from cryptools import *

pub = RSA.importKey(open('pubkey.pem','r').read())
n = pub.n
e = pub.e
flag = s2n(open('flag.enc','rb').read()) 
count = 0
flag += count*n
while True :
    if nroot(flag, 3)[1]:
        print(count)
        print(n2s(nroot(flag , 3)[0]))
        break
    if count % 10000 == 0 :
        print(count)
    count += 1
    flag += n

# count = 118719488
```
### Flag : PCTF{Sm4ll_3xpon3nt_i5_W3ak}