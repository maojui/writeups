
# IOU

這題一堆廢話 XDD

重點是這個 sign 不是 signature，只是單純 pow(m,d,n)

```python
def _sign(self, m):   # alias for _decrypt
    if not self.has_private():
        raise TypeError("No private key")
    return self._decrypt(m)
```

而 verify，也很單純 pow(m,e,n)

```python
def _verify(self, m, sig):
    return self._encrypt(sig) == m
```

只要騙過這個，再讓 int(temp.split()[3]) > 10 就行了

所以有 e、n，就足夠了

```python
while True :
    signature = os.urandom(2048//10)
    temp = pow(s2n(signature),e,n)
    temp = long_to_bytes(temp)
    try :
        if int(temp.split()[3]) > 10 :
            break
    except :
        pass
```

### AIS3{D0cT0R StRaNG3 - F0rgERy ATTaCk Ag4InsT RSa DIgital SigNatUrE}
