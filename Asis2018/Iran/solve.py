from cryptools import *
from cryptools.RSA import *
from sympy import *

key1 = RSAKey.load_pem(b'''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQt5IN0XusElxNCZ3pj5YlTtqZiq
dORNqKaBilvYRmreqtHtX2MD5y3X3PShmF/eyC+Sz2EMHZVrWRNHW4mz7U1EcaDd
tVLQdnl1rB/wI+3dqr+3PTBAJ5uVQs/h7XxMjsxAFMxYFBmVze7gpyRRPXFPWP9K
4idj49HtS4rzKiRwXQIDAQAB
-----END PUBLIC KEY-----
''')

enc_0 = 'BhCIhvtUQ63ItrnxPRFitkasBZMN1215gqvQb8QYA+bGyQiDrJnamT77HgsA3IkyEzow7E5YXQ+hoZ9H7+YPeqlc03B0UUx2peJ5qXzAd9GTeG/5idghU8z46j0PfdZViD3d26PDlA4xrUXa3cY3IZppIz9/Mk+G8CWchnjs2YPX'
c0 = s2n(b64d(enc_0))
print(f'[+] Cipher (c0): {c0}')
key2 = RSAKey.load_pem('''
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgPcib8EOESK34G9gAJx1
tapkjVSfe0E/7aiQtEIaamZv7JqBKucodEQP5w82sFECefpxj+aUfogURyyRAGxm
/t875h8RSHG97CUyJd1KYwR2NOzmfhAc/0jSNi61LZzaRuvpSNIvQowks2tLDEN8
Nh11Z0PNuz7xDygUHB9pG3Cc7ExAGv2hbr7gcUgAxxaiCnMIaVxF8sgRhkaV5nPB
yO2pQ2BjtTvHbsygC2JwaT/MdIwk04/yV4xJvRJOQOwR5M0mXEvepP5YzB9P1pZa
lkGGO9Y3RNZBjmmNzAWNQWxTuMtfHjnxM5LY295yXyVStuexi6tsiA+7oGys96pm
vQIDAQAB
-----END PUBLIC KEY-----
''')

enc_1 = 'CO6jB7EkhdZ6tpIXTjj/kXXFPFA1fddECSV4rxrrsg0TLE/ptCn+e9lm9TBvodltY87C2uH3/mP1evfIsaoxLzcX0tIPl16XCtuEYLkTQ+4S8vz7BQae5N7grivEUzh4T/EyF1Zf2s5zyDEZCorPXWj+Xd0Qc2OwfoQ8+jpJ5znalsaTId0Z7ZI3z8BpWGF5bxVmvTOsNRf6G1PRYn9oI84WIaqbetW0OyoQBbGqzQApWk9fhbZVHxlaRk/+KouyQ1eLNZpvh1j7j2nJx3a7Lda4xP9/sdSrvKyVndYWZuKeZ1Bg3uHuf/gQMa+o0CJrVUuTjMjMq1xFVTs1h1ooeA=='
c1 = s2n(b64d(enc_1))
print(f'[+] Cipher (c1): {c1}')

q = 90829988108297459126723951986073924022504128225586222454376617387900632408868147010157825639889602300446053601539575136123106704382046836252729190919472251
p = key1.n//q
key1.set_private(p,q)
flag0 = n2s(key1.decrypt(c0))

N = key2.n

# # sage
# r_s_min = max(p.previous_prime(), (q.previous_prime()>>2)+1)
# r_s_max = min(p1-1, q1>>2)
rps_min , rps_max = [22707497027074364781680987996518481005626032056396555613594154346975158102217036752539456409972400575111513400384893784030776676095511709063182297729867955, 22707497027074364781680987996518481005626032056396555613594154346975158102217036752539456409972400575111513400384893784030776676095511709063182297729868062]

for rps in range(rps_min, rps_max):
    # solve x**2+(r+s-1)*x+((r+s)**2+(r+s)+1-N) = 0
    x   = Symbol('x')
    krs = solve(x**2 + (rps-1) * x +  rps**2 + rps + 1 - N, x )
    rs = int(max(krs).round())
    rms = nroot(pow(rps,2) - 4*rs,2)
    r = ( rps + rms )//2
    s = ( rps - rms )//2
    p = pow(r,2) + r + 1
    q = pow(s,2) + s + 1
    if isprime(r) + isprime(s) + isprime(p) + isprime(q) == 4 :
        break

r = 12499634052322197156517113844570074858063070132180093106949981756315114873173955244125349117851113985103413267665336997816163464207102752932176612131841251
s = 10207862974752167625163874151948406147562961924216462506644172590660043229043081508414107292121286590008100132719556786214613211888408956131005685598026799
p = 156240851441972631802221590872365199548433251427920958861525362326561429385229704503678026122109494099033132273746193481805470952959264526942790128361011138938521756301147040476473263577899760465829409316910880775950966399157885433015477980346046385388892181847745614165640358705448231145462307601951597086253
q = 104200466511316172778869399412484232432410577006734517689040806370664632008414169969876197410209734803078366536335955234365028495924842514540398861721394984700616799057849702480143488978231977381728134018264755205067162244435476000113140356804090143668453486397378604853972171073327866641690391346367920213201

key2.set_private(p,q)
flag1 = n2s(key2.decrypt(c1)) 
print(flag0+flag1)