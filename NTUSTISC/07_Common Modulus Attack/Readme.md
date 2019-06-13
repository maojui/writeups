## 07Common Modulus Attack_1 :

Get two pair of N,e,c in json :
```python
import random
e = [0xc2eac4c2b,0x15ef25e10f54a3,0x1da0ca25f5a8d,0xc2eac4c2b,0x1a6c23,0x2beccafd,0x280554063943,0x23b0d,0x6b8a5ae7,0x360f1c91fed,0xefe30ec7dabb,0x753fdb5,0x12546aff963f4b6b35f,0x11d2843e693,0x9d540226f,0xee4c39df4ed4c0f,0x213901ef4052b8b251c3,0xe93f,0x4042c3955,0x61553816b407935]

while True:
    e1,e2 = random.choices(e,k=2)
    a,b,c = xgcd(e1,e2)
    if c == 1 :
        break
# e1 = 0x4042c3955, c1 = 0x8caeaa7d272f9606fee9222efd1d922143db738b95bd64746b27bc4c0fd979a2c57b4735131a4391a81bf5f0c0c8eea41d4f91bed4d17784b1956fd89882b97c98009051ac3a03964499c864524d3ddc10299c0290e91707b62ce89b118afe558151be39d61de0483def52c6cb546132ecab85143715bc593a2892b1e41b37b9
# e2 = 0x6b8a5ae7, c2 = 0x6fdcbfb5cd2cacd032ef7200fd49b9f304a6dbd8399f4a91a72d1d9150f97b3b513f44dfc56f6f7c8ec41a8ef9b93a80230a1e65e29d2ef519bb83931d4b0c7a589059cfdf2d571660ab790a9c7e085e3018bf19748abd6d521952b68bc9594c1ad34726658bd9bd445d3b6381ceee57328838e8a129867e505be0ca0d1a1da5
# n = 0xa5f7f8aaa82921f70aad9ece4eb77b62112f51ac2be75910b3137a28d22d7ef3be3d734dabb9d853221f1a17b1afb956a50236a7e858569cdfec3edf350e1f88ad13c1efdd1e98b151ce2a207e5d8b6ab31c2b66e6114b1d5384c5fa0aad92cc079965d4127339847477877d0a057335e2a761562d2d56f1bebb21374b729743
n2s(pow(c1,a,n)*invmod(pow(c2,abs(b),n),n)%n)

```
`Flag : flag_Strength_Lies_In_Differences`

## 07Common Modulus Attack_2 :

```
a,b,c = xgcd(e1,e2)
assert c==1 and a>b
n2s(pow(c1,a,N)*invmod(pow(c2,abs(b),N),N)%N)
```
`Flag : gigem{c0mm0nly_knOwn_AS__bb90200cdb4ac55f}`

## 07Common Modulus Attack_3 :

```
a,b,c = xgcd(e1,e2)
assert c==1 and a<b
n2s(invmod(pow(c1,abs(a),n),n)*pow(c2,b,n)%n)
```
`Flag : CTF{DO NOT SHARE MODULUS PLZ ><!! <>< I AM FISH (?)}`
