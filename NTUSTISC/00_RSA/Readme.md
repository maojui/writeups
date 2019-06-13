## 00RSA?_1 

```
n2s(pow(c,invmod(e,phi),N))
```
`Flag : IceCTF{rsa_is_awesome_when_used_correctly_but_horrible_when_not}`

## 00RSA?_2

```
n2s(c)
```
`Flag : IceCTF{falls_apart_so_easily_and_reassembled_so_crudely}`

## 00RSA?_3

```
n2s(pow(c,invmod(e,(p-1)*(q-1)),p*q))
```
`Flag : ALEXCTF{RS4_I5_E55ENT1AL_T0_D0_BY_H4ND}`

## 00RSA?_4

```
pow(150815,1941,435979)
```
`Flag : 133337`

## 00RSA?_5

```
n2s(pow(c,invmod(e,(p-1)*(q-1)),n))
```
`Flag : simple_rsa_decryption`