# RSA

由題目內容可以發現

```
p = getPrime(512)
q1 = next_prime(2 * p)
q2 = next_prime(3 * q1)
n = p * q1 * q2
```

他的 n 其實是算出來的
我們可以把他推回來

p * q1 * q2 ≒ 12p**3

1. [開三方二分艘](./solve.py)
2. [把誤差算出來]((./solve.py))

算出來就是簡單的解 RSA 了