
import berlekamp
import base64
import binascii
from cytro.sym import Berlekamp_Massey_algorithm
from libnum import *

enc = 'JKIzJOCdeCZhSlxv8OestLzPVKWCQ+wNtfk0LzwezSKjoe09EBB6QRyH8gYS9lrHLAk0DpSdBhwKE8ZgMclbDNXiHcG91V2+IA0bFmi+W2hDMYvThBVlkT6XkFb2s2lSzWL4+v0lKJRzfKrQksOBzBOMYF2RWrbxWIJWQuMWMzE0UCpq5tYnu7me06jDD/UFvpO+LfLmjwgYWTo4CPw1GqeGVVFt2klC2GE='
c = binascii.hexlify(base64.b64decode(enc))
binary = bin(int(c,16))[2:]
n = 0
first = ord('<')^int('0'*n + binary[:6-n],2) 
reg = []
[reg.insert(0,int(b)) for b in bin(first)[2:].rjust(6,'0')]
tmp = ('00' + binary)[8:]
c = [ int(tmp[i]) for i in range(0,len(tmp),8)]
(poly, span, f) = berlekamp.Berlekamp_Massey_algorithm(c)
branches = int(''.join(['1' if i in f else '0' for i in range(max(f)+1)])[::-1],2)
class LFSR:
    
    def __init__(self, register, branches):
        self.register = register
        self.branches = branches
        self.n = len(register)

    def next(self):
        ret = self.register[self.n - 1]
        new = 0
        new = bin(self.branches & int(''.join(map(str,self.register)),2)).count('1') %2
        self.register = [new] + self.register[:-1]
        return ret

register = [ 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,][::-1]
branches = int('1101101110100011',2)
lfsr = LFSR(register, branches)
seq = []
for i in range(60000) :
    seq.append(lfsr.next())
period = pow(2,16) - 1

m = 8
mi = invmod(m,period)
keystream = [None] * (len(binary)-6)
assert gcd(m,period) == 1
for i in range(len(binary)-6):
    if i < 100 :
        print('b' + str(i), '= c' + str((i * mi) % period))
    keystream[i] = seq[(i * mi) % period]
keystream = reg[::-1] + keystream

plaintxt = ''
for i,b in enumerate(binary) :
    plaintxt += str(int(b) ^ keystream[i])
    
print(b2s('00'+plaintxt),)
