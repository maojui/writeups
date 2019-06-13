# POW (1)

很單純的，Hash Collision。

```python
for c in itertools.product(string.digits + string.ascii_letters, repeat=6):
    count += 1
    tail = switchBS(''.join(c))
    if hashlib.sha256(start + tail).hexdigest().startswith('000000'):
        print("Solved.")
        pass_pow = True
        conn.sendline(start + tail)
        break
``` 

### AIS3{Spid3r mAn - H3L1O wOR1d PrO0F 0F WOrK}