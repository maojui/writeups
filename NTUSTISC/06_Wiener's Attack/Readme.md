## 06Wiener's Attack_1 : 

```
p,q = wiener(key.e,key.n)
d = invmod(key.e,(p-1)*(q-1))
n2s(pow(c,int(d),int(p*q)))
```
`Flag : BCTF{9etRea4y!}`

## 06Wiener's Attack_2 : 

```
p,q = wiener(e,n)
d = invmod(e,(p-1)*(q-1))
n2s(pow(c,int(d),int(p*q)))
```
`Flag : flag{Are_any_RSA_vals_good_15878570577}`

## 06Wiener's Attack_3 :

```
RSAKey.load_file('key.public')
p,q = wiener(key.e,key.n)
d = invmod(key.e,(p-1)*(q-1))
```
`Flag :{shorter_d_is_quicker_but_insecure}`
