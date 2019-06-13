from cytro import *
from cytro.sym import *

header = b'\x89PNG\r\n\x1a\n'

for tlen in range(1,100):
    a = b64e(header)
    b = open('enc.png','rb').read()
    b = bytes.fromhex(b.decode())   
    tt = s2b(xor_string(a,b))

    # tlen = i
    s = [int(m)for m in tt[:tlen]]
    _, reglen, taps = Berlekamp_Massey_algorithm(s)
    # print(_)
    # print(reglen)
    register = [int(b) for b in tt[:reglen] ]
    taps = list(taps)[:-1]
    lfsr = LFSR(register,taps)
    c = ''
    for _ in range(len(b)*8):
        c += str(lfsr.next())
    c = B2s(b2s(c))

    a = xor_string( n2s(s2n(b)), c)
    # print(a[:30])

    try :
        a = b64d(a)
        if a[:len(header)] == header :
            with open('flag.png','wb') as png :
                print(tlen)
                print("yep")
                png.write(a)
            break
    except:
        pass