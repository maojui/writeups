import hashlib

avaliable = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def pow(postfix, val):
    for a in avaliable :
        print(chr(a))
        for b in avaliable :
            for c in avaliable :
                for d in avaliable :
                    xxxx = bytes([a,b,c,d])
                    if hashlib.sha256( xxxx + postfix).hexdigest() == val :
                        return xxxx
                
print(pow(b'gOOLfwTfPlnBwRHH','fe2cce38b950f15fbb067448f5168fa236a43816759f1a2d2705d8fc901359b4'))
