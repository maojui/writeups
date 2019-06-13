
# XOR (2)

關鍵就是 `flag.startswith(b'AIS3{')`

與密文 XOR 可得到 key 的前五 byte 為 : `\x16\t|\xc7\xdd`

```python3
length = 0
counter = 0

for i in range(8,13):   # keylen = 8~12
    printable = sum([xor(enc,key+b'x'*(i-5)).count(switchBS(c)) for c in string.printable])
    if printable > counter :
        length = i
        counter = printable
```        

解出最多可視字的 key 長度為 10 

密文長度為 161 -> 後 10 bytes 是 key

最後的 10 bytes 為兩個 key XOR

key : 0 1 2 3 4 5 6 7 8 9 
key : 1 2 3 4 5 6 7 8 9 0

有了 `0 1 2 3 4` 可以算出 `9` 
有 `9` 可以算出 `8` 
...
 
key 為 `\x16\t|\xc7\xdd\x4f\x2e\x92\Xa7\xff`

### AIS3{captAIn aMeric4 - Wh4T3V3R HapPenS t0mORr0w YOU mUst PR0Mis3 ME on3 tHIng. TH4T yOu WiLL stAY Who Y0U 4RE. Not A pERfect sO1dIER, buT 4 gOOD MAn.}
