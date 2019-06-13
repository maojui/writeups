from cryptools import *
import string

enc = open('flag-encrypted','rb').read()
key = xor(enc,"AIS3{")[:5]

length = 0
counter = 0

for i in range(8,13):   # keylen = 8~12
    printable = sum([xor(enc,key+b'x'*(i-5)).count(switchBS(c)) for c in string.printable])
    if printable > counter :
        length = i
        counter = printable

assert len(enc) % length != 0 

# \x16\t|\xc7\xdd\x4f\x2e\x92\Xa7\xff

xor(enc,key+b'\x4f\x2e\x92\xa7\xff')

# AIS3{captAIn aMeric4 - Wh4T3V3R HapPenS t0mORr0w YOU mUst PR0Mis3 ME on3 tHIng. TH4T yOu WiLL stAY Who Y0U 4RE. Not A pERfect sO1dIER, buT 4 gOOD MAn.}