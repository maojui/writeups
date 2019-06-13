from Crypto.PublicKey import RSA
# from primefac import williams_pp1, modinv
from libnum import *

def main():
    pub = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDVRqqCXPYd6Xdl9GT7/kiJrYvy
8lohddAsi28qwMXCe2cDWuwZKzdB3R9NEnUxsHqwEuuGJBwJwIFJnmnvWurHjcYj
DUddp+4X8C9jtvCaLTgd+baSjo2eB0f+uiSL/9/4nN+vR3FliRm2mByeFCjppTQl
yioxCqbXYIMxGO4NcQIDAQAB
-----END PUBLIC KEY-----
"""
    pub = RSA.importKey(pub)
    print(pub.e, pub.n)
    p = 11807485231629132025602991324007150366908229752508016230400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
    # p2 = 12684117323636134264468162714319298445454220244413621344524758865071052169170753552224766744798369054498758364258656141800253652826603727552918575175830897
    print(pub.n)
    q = pub.n // p
    print(p,q)
    assert pub.n == p * q
    priv = RSA.construct((pub.n, pub.e, invmod(pub.e, (p - 1) * (q - 1))))
    with open('spcap_private_key','wb') as f:
        f.write(priv.exportKey('PEM'))


main()