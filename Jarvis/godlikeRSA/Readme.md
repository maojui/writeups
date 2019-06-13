# God like RSA

given a candidate for (p mod 16**(t - 1)), generate all possible candidates for (p mod 16**t) (check against mask for prime1)
calculate q = n * invmod(p, 16**t) (and check against mask for prime2)
calculate d = invmod(e, 16**t) * (1 + k * (N - p - q + 1)) (and check against mask for private exponent)
calculate d_p = invmod(e, 16**t) * (1 + k_p * (p - 1)) (and check against mask for exponent1)
calculate d_q = invmod(e, 16**t) * (1 + k_q * (q - 1)) (and check against mask for exponent2)
if any of checks failed - check next candidate

```bash
openssl rsautl -decrypt -in flag.enc -out flag.txt -inkey privatekey.pem -oaep
```

### FLAG : PCTF{0h_U_r_ju5t_lik3_g0d}