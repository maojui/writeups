from simon import SimonCipher
from libnum import *

plaintxt = 0x6d564d37426e6e71
ciphertxt = 0xbb5d12ba422834b5
block_size = 64
key_size = 96

S = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgihjklmnopqrstuvwxyz0123456789_'

for a in S[-5:] :
    for b in S :
        print(a+b+"..")
        for c in S :
            for d in S :
                key = s2n('SECCON{%s}' % str(a+b+c+d))
                if a+b+c+d == 'FLAG' :
                    print(key)

                cryp = SimonCipher(key, key_size, block_size, 'ECB')
                if plaintxt == cryp.decrypt(ciphertxt) :
                    print("?????")
                    print(a+b+c+d)
                    exit(1)

key == "SECCON{6Pz0}"

# flag = 'FLAG'
# key = s2n('SECCON{%s}' % flag)
# print(key)
# cryp = SimonCipher(key, key_size, block_size, 'ECB')
# cipher = cryp.encrypt(plaintxt)
# plaintxt = cryp.decrypt(ciphertxt)
# print(cipher)
# print(plaintxt)
    
# while True :
#     flag = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ_') for _ in range(4)])
#     key = s2n("SECCON{%s}" % flag)
#     print(flag)
#     # print(key)
#     c = SpeckCipher(key, key_size, block_size, 'ECB')
#     cipher = c.encrypt(plaintxt)
    
#     if plaintxt == c.decrypt(ciphertxt) :
#         print(flag)
#         break