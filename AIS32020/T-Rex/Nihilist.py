import random

a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'         

b = list(a)
random.shuffle(b)

symbol = '!@#$%&'

[print('\t'+s, end='') for s in symbol]
print(end="\n\n")
encoder = {}
decoder = {}
counter = 0
for sy in symbol :
    print(sy + '\t', end="")
    for sx in symbol :
        print(b[counter]+"\t", end="")
        encoder[b[counter]] = sx+sy
        decoder[sx+sy] = b[counter]
        counter += 1
    print(end="\n\n")

def encode(a) :
    if a in encoder.keys():
        return encoder[a]
    else :
        return a

def decode(a) :
    if a in decoder.keys():
        return decoder[a]
    else :
        return a


flag = f"AIS3{{Tyr4nn0s4uru5_r3x_giv3_y0U_something_random_{''.join([random.choice(b) for _ in range(200)])}}}".upper()
enc = ' '.join([encode(c) for c in flag])  

print(flag)
print(enc)

dec = ''.join([decode(sym) for sym in enc.split(' ')])
assert flag == dec

# AIS3{C210RYU0QFP1VX0FOHSKUZWX3M9LLL96KKG5Q30P1I3JZ2Y8RVW2FEYI1VQSOI654DYMKE03039NBNH18O7FJR3YUY3N38EPWNWREHJN5VT1ETLSXDDX9Q9FQ85YKSJQDBFFXKBRFA162ETH0YX4CTRMAPQTFYVMX3DSRM7IL0373LEJ930QIDN8CTYHKA3KI6KO2FIOJC6NKQIY1C05RN42LMDWQNTKTUYSV9K0QX8SV1FDI9FDPMVF6JDZP5KN}