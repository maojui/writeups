from Crypto.PublicKey import RSA
from cryptools import *

with open('pubkey.pem','r') as pubkey :
    key = pubkey.read()
    pub = RSA.importKey(key)
    n = pub.n
    e = pub.e
    p = 275127860351348928173285174381581152299
    q = pub.n//p
    assert n == p*q
    phi = (p-1)*(q-1)
    
    with open('flag.enc','rb') as file :
        flag = s2n(file.read())
        r1 = list(sqrtmod_prime_power(flag,p,1))
        r2 = list(sqrtmod_prime_power(flag,q,1))
        for a in r1 :
            for b in r2 :
                print(n2s(solve_crt([a,b],[p,q])))
        
    #Flag : PCTF{sp3ci4l_rsa}