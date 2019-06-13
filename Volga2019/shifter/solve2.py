import binascii
from cytro import *
from cytro.sym import *

enc = 'JKIzJOCdeCZhSlxv8OestLzPVKWCQ+wNtfk0LzwezSKjoe09EBB6QRyH8gYS9lrHLAk0DpSdBhwKE8ZgMclbDNXiHcG91V2+IA0bFmi+W2hDMYvThBVlkT6XkFb2s2lSzWL4+v0lKJRzfKrQksOBzBOMYF2RWrbxWIJWQuMWMzE0UCpq5tYnu7me06jDD/UFvpO+LfLmjwgYWTo4CPw1GqeGVVFt2klC2GE='
c = binascii.hexlify(base64.b64decode(enc))
enc = b2s('00' + bin(int(c,16))[2:])
offset = 0

for offset in range(0,len(enc)):
    a = 'VolgaCTF{'
    tt = s2b(xor_string(a,enc[offset:]))
    tlen = 100
    s = [int(m) for m in tt[:tlen]]
    _, reglen, taps = Berlekamp_Massey_algorithm(s)
    register = [int(b) for b in tt[:reglen] ]
    taps = sorted(list(taps))[:-1]
    lfsr = LFSR(register,taps)
    c = ''
    for _ in range( 8*len(enc[offset:]) ):
        c += str(lfsr.next())
    c = b2s(c)
    a = xor_string( enc[offset:], c)
    if a[-1] == '>' :
        print(a)

