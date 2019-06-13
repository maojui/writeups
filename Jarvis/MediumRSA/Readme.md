
# Medium RSA

Standard RSA ... JUST SOLVE IT !!!!!

```python
from Crypto.PublicKey import RSA
from cryptools import *

pub = RSA.importKey(open('pubkey.pem','r').read())    
n = pub.n
p = 275127860351348928173285174381581152299
q = pub.n//p
phi = (p-1)*(q-1)
e = pub.e
d = invmod(e,phi)

flag = s2n(open('flag.enc','rb').read())
flag = n2s(pow(flag,d,n))
print(flag)
```

### Flag : PCTF{256b_i5_m3dium}